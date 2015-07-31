from django import forms
from . import models

class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ('name',)
        widgets = {'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Name this game"})}
        
class BudgetForm(forms.ModelForm):
    def clean_svc_health(self):
        data = self.cleaned_data['svc_health']
        if self.instance.debt_wbsap and data > 15:
            raise forms.ValidationError('SAP limits health spending to 15%.')
        return data
    
    def clean_svc_security(self):
        data = self.cleaned_data['svc_security']
        if self.instance.debt_wbsap and data > 20:
            raise forms.ValidationError('SAP limits security spending to 15%.')
        return data
        
    class Meta:
        model = models.Turn
        fields = ('tax_cocoa', 'tax_lower', 'tax_upper', 'svc_health', 'svc_education', 'svc_security',)
        labels = {'tax_cocoa':'Cocoa Tax',
                  'tax_lower':'Income Tax - Lower Bracket',
                  'tax_upper':'Income Tax - Upper Bracket',
                  'svc_health':'Healthcare Funding',
                  'svc_education':'Education Funding',
                  'svc_security':'Security Funding',}
        
class CropsForm(forms.ModelForm):
    def is_valid(self):
        valid = super(CropsForm, self).is_valid()
        if self.cleaned_data.get("corn")+self.cleaned_data.get("cocoa") > self.instance.land:
            self._errors['insufficient_land'] = 'Total planted area cannot exceed {0} kha.'.format(self.instance.land)
            valid = False
        return valid
    
    class Meta:
        model = models.Turn
        fields = ('pesticides', 'corn', 'cocoa',)
        
class DebtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', {})
        if instance:
            initial['debt_repay_private'] = int(instance.debt_repay_private/10**6)
            initial['debt_repay_wb'] = int(instance.debt_repay_wb/10**6)
            initial['debt_repay_wbsap'] = int(instance.debt_repay_wbsap/10**6)
            kwargs['initial'] = initial
        super(DebtForm, self).__init__(*args, **kwargs)
    
    def clean_debt_repay_private(self):
        data = self.cleaned_data['debt_repay_private']*10**6
        if data > self.instance.debt_private:
            raise forms.ValidationError("You cannot repay more debt than you have.")
        return data
        
    def clean_debt_repay_wb(self):
        data = self.cleaned_data['debt_repay_wb']*10**6
        if data > self.instance.debt_wb:
            raise forms.ValidationError("You cannot repay more debt than you have.")
        return data
        
    def clean_debt_repay_wbsap(self):
        data = self.cleaned_data['debt_repay_wbsap']*10**6
        if data > self.instance.debt_wbsap:
            raise forms.ValidationError("You cannot repay more debt than you have.")
        return data
    
    class Meta:
        model = models.Turn
        fields = ('debt_repay_private', 'debt_repay_wb', 'debt_repay_wbsap',)
        labels = {'debt_repay_private':'Repay Private Debt',
                  'debt_repay_wb':'Repay World Bank Debt',
                  'debt_repay_wbsap':'Repay World Bank SAP Debt',}
        