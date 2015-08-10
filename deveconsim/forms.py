import math

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText, PrependedAppendedText, FormActions

from . import models

class GameForm(forms.Form):
    def __init__(self, open_games, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        if len(open_games) > 1:
            self.fields['continue_game'] = forms.ChoiceField(required=False, choices=[(None,'Start a new game')]+[(g.pk,'Resume g'+str(g)[1:]) for g in open_games])
        else:
            self.fields['continue_game'] = forms.IntegerField(required=False, widget=forms.HiddenInput())
        self.fields['name'] = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder':"Name your new game"}))
    
class TurnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TurnForm, self).__init__(*args, **kwargs)
        
        #add validation in the form of clean_[field] functions
        self.clean_debt_repay_private = self.clean_debt_repay('private',10**6)
        self.clean_debt_repay_wb = self.clean_debt_repay('wb',10**6)
        self.clean_debt_repay_wbsap = self.clean_debt_repay('wbsap',10**6)
        self.clean_svc_health = self.clean_svc_sap('health',15)
        self.clean_svc_security = self.clean_svc_sap('security',20)
        
        #scale initial values
        self.initial['debt_repay_private'] = int(self.instance.debt_repay_private/10**6)
        self.initial['debt_repay_wb'] = int(self.instance.debt_repay_wb/10**6)
        self.initial['debt_repay_wbsap'] = int(self.instance.debt_repay_wbsap/10**6)
        
        #add calculated fields/help text
        calc = self.instance.calc()
        self.initial['debt_new_wbsap'] = int(calc['debt_new_wbsap_max']/10**6)
        self.initial['wbsap_cocoa'] = calc['wbsap_add_cocoa']
        if 'corn' in self.fields :
            self.fields['corn'].help_text = 'Was {0} kha'.format(self.instance.start_corn)
        if 'cocoa' in self.fields:
            self.fields['cocoa'].help_text = 'Was {0} kha'.format(self.instance.start_cocoa)
        if 'svc_health' in self.fields and self.instance.debt_wbsap:
            self.fields['svc_health'].help_text = '15% SAP limit'
        if 'svc_security' in self.fields and self.instance.debt_wbsap:
            self.fields['svc_security'].help_text = '20% SAP limit'
        if 'debt_repay_private' in self.fields:
            self.fields['debt_repay_private'].help_text = 'Owe ${0} M'.format(math.ceil(self.instance.debt_private/10**6))
        if 'debt_repay_wb' in self.fields:
            self.fields['debt_repay_wb'].help_text = 'Owe ${0} M'.format(math.ceil(self.instance.debt_wb/10**6))
        if 'debt_repay_wbsap' in self.fields:
            self.fields['debt_repay_wbsap'].help_text = 'Owe ${0} M'.format(math.ceil(self.instance.debt_wbsap/10**6))
        if 'debt_new_wbsap' in self.fields:
            if calc['new_genfund'] >= 0:
                self.fields['debt_new_wbsap'].widget = forms.HiddenInput()
            else:
                self.fields['debt_new_wbsap'].help_text = '${0} M - ${1} M'.format(math.ceil(calc['debt_new_wbsap_min']/10**6),self.initial['debt_new_wbsap'])
        
        #set up crispy_forms helper
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        button_text = 'End Turn' if 'debt_new_wbsap' in self.fields else 'Update'
        self.helper.layout.append(FormActions(Submit('submit', button_text)))
        
    def clean_debt_repay(self,type,mult=1): #totally unecessary use of functional programming
        def clean_debt_repay_type():
            value = self.cleaned_data['debt_repay_'+type]*mult
            if value > getattr(self.instance,'debt_'+type):
                raise forms.ValidationError('Cannot repay more debt than you owe.')
            return value
        return clean_debt_repay_type
        
    def clean_svc_sap(self,type,sap_max):
        def clean_svc_type():
            value = self.cleaned_data['svc_'+type]
            if self.instance.debt_wbsap and value > sap_max:
                raise forms.ValidationError('Exceeds {0}% World Bank SAP limit.'.format(sap_max))
            return value
        return clean_svc_type
        
    def clean_debt_new_wbsap(self):
        value = self.cleaned_data['debt_new_wbsap']*10**6
        calc = self.instance.calc()
        if value > calc['debt_new_wbsap_max']:
            raise forms.ValidationError('The World Bank is only willing to lend to cover interest on World Bank loans.')
        return value
        
    def clean(self):
        cleaned_data = super(TurnForm, self).clean()
        calc = self.instance.calc()
        errs = []
        if 'corn' in cleaned_data and 'cocoa' in cleaned_data:
            if cleaned_data['corn'] + cleaned_data['cocoa'] > self.instance.land:
                errs.append('Total planted area cannot exceed {0} kha.'.format(self.instance.land))
        if 'debt_new_wbsap' in cleaned_data:
            if calc['new_genfund'] + cleaned_data['debt_new_wbsap'] < 0:
                errs.append('Your general fund may not drop below zero.')
        if errs:
            raise forms.ValidationError(errs)
        
    class Meta:
        model = models.Turn
        fields = ('debt_new_wbsap','wbsap_cocoa','corn','cocoa','svc_health','svc_education','svc_security','debt_repay_private','debt_repay_wb','debt_repay_wbsap',)

class CropsForm(TurnForm):
    def __init__(self, *args, **kwargs):
        super(CropsForm, self).__init__(*args, **kwargs)
        self.helper['corn'].wrap(AppendedText, 'kha')
        self.helper['cocoa'].wrap(AppendedText, 'kha')
        
    class Meta(TurnForm.Meta):
        fields = ('pesticides', 'corn', 'cocoa',)
        
class BudgetForm(TurnForm):
    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.helper.all().wrap(AppendedText, '%')
        
    class Meta(TurnForm.Meta):
        fields = ('tax_cocoa', 'tax_lower', 'tax_upper', 'svc_health', 'svc_education', 'svc_security',)
                
class DebtForm(TurnForm):
    def __init__(self, *args, **kwargs):
        super(DebtForm, self).__init__(*args, **kwargs)
        self.helper.all().wrap(PrependedAppendedText, '$', 'M')
        
    class Meta(TurnForm.Meta):
        fields = ('debt_repay_private', 'debt_repay_wb', 'debt_repay_wbsap',)
                  
class EndTurnForm(TurnForm):
    def __init__(self, *args, **kwargs):
        super(EndTurnForm, self).__init__(*args, **kwargs)
        self.helper['debt_new_wbsap'].wrap(PrependedAppendedText, '$', 'M')
        self.helper['submit'].wrap(Submit,'End Turn')
        
    class Meta(TurnForm.Meta):
        fields = TurnForm.Meta.fields
        widgets = dict((k,forms.HiddenInput(attrs={'readonly':True})) for k in fields if k != 'debt_new_wbsap')