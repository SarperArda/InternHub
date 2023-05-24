from django import forms
from users.models import EngineeringDepartment, Course
from company.models import Company, CompanyApprovalValidationApplication
from django.core.exceptions import ValidationError


class CompanyForm(forms.ModelForm):
    departments = forms.ModelMultipleChoiceField(
        queryset=EngineeringDepartment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Company
        fields = ['name', 'field', 'departments']


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Company.objects.filter(name__iexact=name).exists():
            raise ValidationError('A company with this name already exists.')
        return name

class CAVAForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.RadioSelect,
        required=True,
    )

    requested_company = forms.ModelChoiceField(
        queryset = Company.objects.all(),
        widget=forms.Select,
        required=True,
    )

    class Meta:
        model = CompanyApprovalValidationApplication
        fields = ['course', 'file', 'requested_company']