from django import forms
from . import models
import math

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
        self.clean_debt_repay_private = self.clean_debt_repay('private',10**6)
        self.clean_debt_repay_wb = self.clean_debt_repay('wb',10**6)
        self.clean_debt_repay_wbsap = self.clean_debt_repay('wbsap',10**6)
        self.clean_svc_health = self.clean_svc_sap('health',15)
        self.clean_svc_security = self.clean_svc_sap('security',20)
        self.initial['debt_repay_private'] = int(self.instance.debt_repay_private/10**6)
        self.initial['debt_repay_wb'] = int(self.instance.debt_repay_wb/10**6)
        self.initial['debt_repay_wbsap'] = int(self.instance.debt_repay_wbsap/10**6)
        calc = self.instance.calc()
        self.initial['debt_new_wbsap'] = int(calc['debt_new_wbsap_max']/10**6)
        self.initial['wbsap_cocoa'] = calc['wbsap_add_cocoa']
        if 'debt_new_wbsap' in self.fields and calc['new_genfund'] >= 0:
            self.fields['debt_new_wbsap'].widget = forms.HiddenInput()
        
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
            raise forms.ValidationError('The World Bank is only willing to extend loans to cover interest on loans to them.')
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
    class Meta(TurnForm.Meta):
        fields = ('pesticides', 'corn', 'cocoa',)
        
class BudgetForm(TurnForm):        
    class Meta(TurnForm.Meta):
        fields = ('tax_cocoa', 'tax_lower', 'tax_upper', 'svc_health', 'svc_education', 'svc_security',)
                
class DebtForm(TurnForm):
    class Meta(TurnForm.Meta):
        fields = ('debt_repay_private', 'debt_repay_wb', 'debt_repay_wbsap',)
                  
class EndTurnForm(TurnForm):
    class Meta(TurnForm.Meta):
        fields = TurnForm.Meta.fields
        widgets = dict((k,forms.HiddenInput(attrs={'readonly':True})) for k in fields if k != 'debt_new_wbsap')