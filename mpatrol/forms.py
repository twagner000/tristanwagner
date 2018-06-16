from django import forms

from . import models

class PlayerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.game

class ResumeForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player'] = PlayerModelChoiceField(empty_label=None, queryset=models.Player.objects.filter(user=user, game__ended_date__isnull=True).order_by('-last_action_date','-started_date'))
        
class JoinForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game'] = forms.ModelChoiceField(empty_label=None, queryset=models.Game.objects.filter(ended_date__isnull=True).exclude(pk__in=models.Player.objects.filter(user=user).values('game__pk')).order_by('-started_date'))
        self.fields['character_name'] = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':"Name your character"}))