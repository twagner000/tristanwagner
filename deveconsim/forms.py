from django import forms
from . import models

class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ('name',)
        widgets = {'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Name this game"})}
        
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
        widgets = {'tax_cocoa':forms.TextInput(attrs={'class':'form-control touchspin-pct-30'}),
                   'tax_lower':forms.TextInput(attrs={'class':'form-control touchspin-pct-70'}),
                   'tax_upper':forms.TextInput(attrs={'class':'form-control touchspin-pct-70'}),
                   'svc_health':forms.TextInput(attrs={'class':'form-control touchspin-pct'}),
                   'svc_education':forms.TextInput(attrs={'class':'form-control touchspin-pct'}),
                   'svc_security':forms.TextInput(attrs={'class':'form-control touchspin-pct'}),}
        
class CropsForm(forms.ModelForm):
    class Meta:
        model = models.Turn
        fields = ('pesticides', 'corn', 'cocoa',)
        labels = {'pesticides':'Pesticide Use',
                  'corn':'Area Planted with Corn',
                  'cocoa':'Area Planted with Cocoa',}
        widgets = {'pesticides':forms.Select(attrs={'class':'form-control'}),
                   'corn':forms.TextInput(attrs={'class':'form-control touchspin-ha'}),
                   'cocoa':forms.TextInput(attrs={'class':'form-control touchspin-ha'}),}