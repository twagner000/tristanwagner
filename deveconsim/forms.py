from django import forms
from . import models
import math

class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ('name',)
        widgets = {'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Name this game"})}

class TurnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', {})
        if instance:
            self.clean_debt_repay_private = self.clean_debt_repay('private',10**6)
            self.clean_debt_repay_wb = self.clean_debt_repay('wb',10**6)
            self.clean_debt_repay_wbsap = self.clean_debt_repay('wbsap',10**6)
            self.clean_svc_health = self.clean_svc_sap('health',15)
            self.clean_svc_security = self.clean_svc_sap('security',20)
            initial['debt_repay_private'] = int(instance.debt_repay_private/10**6)
            initial['debt_repay_wb'] = int(instance.debt_repay_wb/10**6)
            initial['debt_repay_wbsap'] = int(instance.debt_repay_wbsap/10**6)
            calc = instance.calc()
            initial['debt_new_wbsap'] = int(calc['debt_new_wbsap_max']/10**6)
            kwargs['initial'] = initial
        super(TurnForm, self).__init__(*args, **kwargs)
        
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
        errs = []
        calc = self.instance.calc()
        if value < calc['debt_new_wbsap_min']:
            errs.append('Not enough to cover budget shortfall.')
        if value > calc['debt_new_wbsap_max']:
            errs.append('World Bank is only willing to extend loans to cover interest on loans to them.')
        if errs:
            raise forms.ValidationError(errs)
        return value
        
    def clean(self):
        cleaned_data = super(TurnForm, self).clean()
        errs = []
        if 'corn' in cleaned_data and 'cocoa' in cleaned_data:
            if cleaned_data['corn'] + cleaned_data['cocoa'] > self.instance.land:
                errs.append('Total planted area cannot exceed {0} kha.'.format(self.instance.land))
        if errs:
            raise forms.ValidationError(errs)
        
    class Meta:
        model = models.Turn
        fields = ('debt_new_wbsap','corn','cocoa','svc_health','svc_education','svc_security','debt_repay_private','debt_repay_wb','debt_repay_wbsap',)

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
                  
                  
                  