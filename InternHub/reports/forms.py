from django import forms
from users.models import EngineeringDepartment, Course, Student
from company.models import Company
from reports.models import Internship
from django.core.exceptions import ValidationError


yes_no_choices = ('Yes', 'Yes'), ('No', 'No')


class ConfidentialCompanyForm(forms.Form):
    student_id = forms.CharField(min_length=8, max_length=8, required=True)
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    company = forms.CharField(
        label="Company Name", max_length=100, required=True)

    department = forms.ModelChoiceField(
        queryset=EngineeringDepartment.objects.all(),
        widget=forms.RadioSelect,
        required=True,
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(),
        widget=forms.RadioSelect,
        required=True,
    )
    grade = forms.IntegerField(min_value=0, max_value=10)
    is_work_related = forms.ChoiceField(
        label="Is the work done related to (department) engineering?",
        choices=yes_no_choices,
        widget=forms.RadioSelect,)
    supervisor_background = forms.ChoiceField(
        label="Is the supervisor's a (department) engineer or has a similar engineering background?",
        choices=yes_no_choices,
        widget=forms.RadioSelect,)

    def clean(self):
        cleaned_data = super().clean()

        # Getting data from the form
        student_id = cleaned_data.get('student_id')
        name = cleaned_data.get('name')
        surname = cleaned_data.get('surname')
        company = cleaned_data.get('company')
        department = cleaned_data.get('department')
        course = cleaned_data.get('course')

        # Checking if the student exists and if the internship exists.
        try:
            student = Student.objects.get(user_id=student_id)
            internship = Internship.objects.get(student=student, course=course)
        except Student.DoesNotExist:
            self.add_error('student_id', 'Student does not exist')
            return
        except Internship.DoesNotExist:
            self.add_error(
                'student_id', f'Internship does not exist ({department.code}{course.code})')
            return
