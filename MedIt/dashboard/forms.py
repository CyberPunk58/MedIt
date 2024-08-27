from django import forms
from .models import Clinic, Revenue, PaymentType

class MonthYearWidget(forms.DateInput):
    input_type = 'month'

    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m'
        super().__init__(**kwargs)

class RevenueForm(forms.ModelForm):
    revenue = forms.DecimalField(label='Revenue', max_digits=10, decimal_places=2)
    date = forms.DateField(widget=MonthYearWidget(), label='Date (Month and Year)', input_formats=['%Y-%m'])
    payment_type = forms.ModelChoiceField(queryset=PaymentType.objects.all(), label='Payment Type')

    class Meta:
        model = Revenue
        fields = ['clinic', 'revenue', 'date', 'payment_type']

