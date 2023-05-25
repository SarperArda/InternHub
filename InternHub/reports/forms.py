from django import forms
from users.models import EngineeringDepartment, Course, Student
from company.models import Company
from reports.models import Internship, Submission, Feedback
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import WorkAndReportEvaluation, ConfidentialCompany

yes_no_choices = ('Yes', 'Yes'), ('No', 'No')
satisfactory_choices = ('Satisfactory','Satisfactory'), ('Revision Required','Revision Required'), ('Unsatisfactory','Unsatisfactory') 


class ConfidentialCompanyForm(forms.ModelForm):
    class Meta:
        model = ConfidentialCompany
        fields = [
            "company_name",
            "grade",
            "is_work_related",
            "supervisor_background",
        ]
        labels = {
            "company_name" :  "Company Name",
            "grade" : "Average of the grades on the Summer Training Evaluation Form ",
            "is_work_related" : "Is the work done related to related engineering department? ",
            "supervisor_background" : """
                                        Is the supervisor is an engineer with a related department title
                                        or has similar background with that engineer?
                                      """

        }
        error_messages = {
            "grade": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0",
            }
        }

    """
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
        """
class SummerTrainingGradingForm(forms.ModelForm):
    instructor_name = forms.CharField(max_length=100)
    instructor_surname = forms.CharField(max_length=100)
    student_name = forms.CharField(max_length=100)
    student_surname = forms.CharField(max_length=100)
    student_id = forms.CharField(min_length=8, max_length=8, required=True)
    partB_satisfactory = forms.ChoiceField(
        choices=[choice for choice in satisfactory_choices if choice[0] != 'Unsatisfactory'],
        widget=forms.RadioSelect,
        required=True,
    )
    date_resubmission = forms.DateTimeField()
    score_evaluation_one = forms.IntegerField(
        label='Assessment/quality score of Evaluation of the Work - item (1)',
        min_value=0, max_value=10
        )
    sum_score_evaluation_except_one = forms.IntegerField(
        label='Sum of the Assessment/quality score of Evaluation of the Work - items (2)-(7)',
        min_value=0, max_value=60
        )
    score_evaluation_report = forms.IntegerField(
        label= 'The Assessment/quality score of Report',
        min_value=0, max_value=10
        )
    partC_evaluation = forms.ChoiceField(
        label='Overall Evaluation',
        choices=[choice for choice in satisfactory_choices if choice[0] != 'Revision Required'],
        widget=forms.RadioSelect,
        required=True,
    )
    date_submission = forms.DateTimeField()
    def clean(self):
        cleaned_data = super().clean()

        # Getting data from the form
        student_id = cleaned_data.get('student_id')
        name = cleaned_data.get('name')
        surname = cleaned_data.get('surname')

        # Checking if the student exists and if the internship exists.
        try:
            student = Student.objects.get(user_id=student_id)
        except Student.DoesNotExist:
            self.add_error('student_id', 'Student does not exist')
            return

class WorkAndReportEvaluationForm(forms.ModelForm):
    class Meta:
        model = WorkAndReportEvaluation
        fields = [
            "grade_of_performing_work",
            "exp_is_able_to_perform_work",

            "grade_of_solving_engineering_problems",
            "exp_is_able_to_solve_engineering_problems",

            "grade_of_recognizing_ethics",
            "exp_is_recognize_ethics",

            "grade_of_making_judgements",
            "exp_is_make_informed_judgments",

            "grade_of_acquiring_knowledge",
            "exp_is_able_to_acquire_knowledge",

            "grade_of_applying_knowledge",
            "exp_is_able_to_apply_new_knowledge",

            "grade_of_has_awareness",
            "exp_has_awareness",

            "grade_of_preparing_reports",
            "exp_is_able_to_prepare_reports",

        ]
        labels = {
            "grade_of_performing_work" : """
                                            Able to perform a work at the level expected from a summer training
                                            in the area of department: 
                                            (This is the evaluation of all work done in summer training)
                                         """ ,
            "exp_is_able_to_perform_work": "Pages on which evidence is found for given grade above",

            "grade_of_solving_engineering_problems": """
                                                        Solves complex engineering problems by applying principles of 
                                                        engineering, science and mathematics:
                                                    """,
            "exp_is_able_to_solve_engineering_problems": "Pages on which evidence is found for given grade above",

            "grade_of_recognize_ethics": """
                                            Recognizes ethical and professional responsibilities in engineering
                                            situations:
                                         """,
            "exp_is_recognize_ethics": "Pages on which evidence is found for given grade above",

            "grade_of_making_judgements": """
                                            Able to make informed judgements that consider the impact of solutions
                                            in global, environmental, societal and economic contexts
                                          """,
            "exp_is_make_informed_judgments": "Pages on which evidence is found for given grade above",

            "grade_of_acquiring_knowledge": "Able to acquire new knowledge using appropriate learning strategies",
            "exp_is_able_to_acquire_knowledge": "Pages on which evidence is found for given grade above",

            "grade_of_applying_knowledge": "Able to apply acquired knowledge as needed",
            "exp_is_able_to_apply_new_knowledge": "Pages on which evidence is found for given grade above",

            "grade_of_has_awareness": "Has awareness about diversity, equity and inclusion",
            "exp_has_awareness": "Pages on which evidence is found for given grade above",

            "grade_of_preparing_reports": """
                                            Able to prepare reports with high standards in terms of content, 
                                            organization and style
                                            (the Summer training report itself to be evaluated)
                                          """,
            "exp_is_able_to_prepare_reports" : "Pages on which evidence is found for given grade above",

        }

        error_messages = {
            "grade_of_performing_work": {
                "max_value" : "Grade cannot be greater than 10",
                "min_value" : "Grade cannot be less than 0",
            },
            "grade_of_solving_engineering_problems": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0",
            },
            "grade_of_recognizing_ethics":  {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0"
            },
            "grade_of_making_judgements": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0"
            },
            "grade_of_acquiring_knowledge": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0"
            },
            "grade_of_applying_knowledge": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0"
            },
            "grade_of_has_awareness": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0"
            },
            "grade_of_preparing_reports": {
                "max_value": "Grade cannot be greater than 10",
                "min_value": "Grade cannot be less than 0"
            },
        }
class StudentReportForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

class ExtensionForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    
    class Meta:
        model = Submission
        fields = ['due_date']

