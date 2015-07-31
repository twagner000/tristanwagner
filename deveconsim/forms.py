from django import forms
from . import models

class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ('name',)
        widgets = {'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Name this game"})}
        
class CropsForm(forms.ModelForm):
    class Meta:
        model = models.Turn
        fields = ('pesticides', 'corn', 'cocoa',)

class BudgetForm(forms.ModelForm):        
    class Meta:
        model = models.Turn
        fields = ('tax_cocoa', 'tax_lower', 'tax_upper', 'svc_health', 'svc_education', 'svc_security',)
        labels = {'tax_cocoa':'Cocoa Tax',
                  'tax_lower':'Income Tax - Lower Bracket',
                  'tax_upper':'Income Tax - Upper Bracket',
                  'svc_health':'Healthcare Funding',
                  'svc_education':'Education Funding',
                  'svc_security':'Security Funding',}
                
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
        return self.cleaned_data['debt_repay_private']*10**6
        
    def clean_debt_repay_wb(self):
        return self.cleaned_data['debt_repay_wb']*10**6
        
    def clean_debt_repay_wbsap(self):
        return self.cleaned_data['debt_repay_wbsap']*10**6
        
    class Meta:
        model = models.Turn
        fields = ('debt_repay_private', 'debt_repay_wb', 'debt_repay_wbsap',)
        labels = {'debt_repay_private':'Repay Private Debt',
                  'debt_repay_wb':'Repay World Bank Debt',
                  'debt_repay_wbsap':'Repay World Bank SAP Debt',}

class EndTurnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', {})
        if instance:
            initial['test'] = 'Test'
            kwargs['initial'] = initial
        super(EndTurnForm, self).__init__(*args, **kwargs)
    
    """def clean_debt_repay_private(self):
        data = self.cleaned_data['debt_repay_private']*10**6
        if data > self.instance.debt_private:
            raise forms.ValidationError("You cannot repay more debt than you have.")
        return data"""
        
    class Meta:
        model = models.Turn
        fields = ('debt_new_wbsap',)
                  
                  
                  
                  
                  
                  