from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Household

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'telegram_chat_id')

class HouseholdCreateForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ('name',)

class HouseholdJoinForm(forms.Form):
    join_code = forms.CharField(max_length=50, required=True, label="Join Code")
