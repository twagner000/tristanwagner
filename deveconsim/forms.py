from django import forms
from . import models

class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ('name',)
        widgets = {'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Name this game"})}
        
class BudgetForm(forms.ModelForm):
    def is_valid(self):
        valid = super(BudgetForm, self).is_valid()
        if self.instance.debt_wbsap and (self.cleaned_data.get("svc_health",100)>15 or self.cleaned_data.get("svc_security",100)>20):
            self._errors['sap_limit'] = "*Due to a Structural Adjustment Program (SAP) to which you agreed as part of a World Bank loan, your health spending is limited to 15% and your security spending is limited to 20%. These restrictions will be lifted once your loan is repaid."
            valid = False
        return valid
        
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
        