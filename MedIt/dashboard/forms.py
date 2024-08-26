from django import forms
from .models import Clinic, Revenue, PaymentType

class RevenueForm(forms.ModelForm):
    revenue = forms.DecimalField(label='Revenue', max_digits=10, decimal_places=2)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'month'}), label='Date (Month and Year)')
    payment_type = forms.ModelChoiceField(queryset=PaymentType.objects.all(), label='Payment Type')

    class Meta:
        model = Revenue
        fields = ['clinic', 'revenue', 'date', 'payment_type']
