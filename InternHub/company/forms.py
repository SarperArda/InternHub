from django import forms
from users.models import EngineeringDepartment
from company.models import Company, CompanyRequest
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
     