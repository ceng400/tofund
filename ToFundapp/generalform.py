from django.forms import ModelForm
from django import forms
from .models import donation, Fund


class donationform(ModelForm):
    class Meta:
        model = donation
        fields = ("amount", "email")


class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['fund_name', 'duration_from', 'duration_to', 'target_amount', 'email', 'Reason_for_fund']
        widgets = {
            'fund_name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_from': forms.DateInput(attrs={'class': 'form-control'}),
            'duration_to': forms.DateInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Reason_for_fund': forms.Textarea(attrs={'class': 'form-control'}),
        }