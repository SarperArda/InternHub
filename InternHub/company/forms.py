from django import forms
from users.models import EngineeringDepartments
from .models import Company


class CompanyForm(forms.ModelForm):
    department_choices = EngineeringDepartments.choices

    department = forms.MultipleChoiceField(
        choices=department_choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Company
        fields = ['name', 'address', 'field', 'city', 'department']
