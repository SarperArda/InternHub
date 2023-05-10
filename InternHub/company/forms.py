from django import forms
from users.models import EngineeringDepartment
from .models import Company


class CompanyForm(forms.ModelForm):
    departments = forms.ModelMultipleChoiceField(
        queryset=EngineeringDepartment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Company
        fields = ['name', 'address', 'field', 'city', 'departments']
