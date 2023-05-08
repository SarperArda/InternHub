from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return HttpResponse("You are viewing home page")


def fill_confidential_company_form(request):
    pass


def student_list(request):
    pass


def instructor_list(request):
    pass


def company_list (request):
    pass


def add_company(request):
    pass


def assign_students_to_instructors(request):
    pass


def list_company_approval_validation_application(request):
    pass


def list_company_request(request):
    pass


def list_company_evaluation_by_student(request):
    pass


def make_announcement(request):
    pass