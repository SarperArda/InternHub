from django.contrib.auth.base_user import BaseUserManager
from users.models import User, Student, Instructor, DepartmentSecretary, Chair, Dean
from users.models import Course, EngineeringDepartment
from company.models import Company, CompanyApprovalValidationApplication,EvaluationByStudent
from reports.models import Internship, Statistic
import json
import random
from users.models import UserManager


class DatabaseManager:
    @staticmethod
    def restart_database():
        DatabaseManager.delete_database()
        DatabaseManager.create_database()

    @staticmethod
    def create_courses():
        with open('fixtures/courses.json') as file:
            data = json.load(file)
            for user in data:
                course = Course(**user['fields'])
                course.save()

    @staticmethod
    def create_departments():
        with open('fixtures/departments.json') as file:
            data = json.load(file)
            for user in data:
                department = EngineeringDepartment(**user['fields'])
                department.save()

    @staticmethod
    def create_companies():
        with open('fixtures/companies.json') as file:
            data = json.load(file)
            for company_data in data:
                cs_pk = EngineeringDepartment.objects.all()[0].pk
                me_pk = EngineeringDepartment.objects.all()[1].pk
                eee_pk = EngineeringDepartment.objects.all()[2].pk
                ie_pk = EngineeringDepartment.objects.all()[3].pk
                company = Company(name=company_data['fields']['name'],
                                    status=company_data['fields']['status'],
                                    field=company_data['fields']['field'])
                company.save()  # Save the company first

                # Refresh the company instance to get the updated values, including the id
                company.refresh_from_db()
                dep_no = company_data['fields']['departments']
                if dep_no == 1:
                    final_pk = cs_pk
                elif dep_no == 2:
                    final_pk = me_pk
                elif dep_no == 3:
                    final_pk = eee_pk
                else:
                    final_pk = ie_pk
                company.departments.add(EngineeringDepartment.objects.all().get(pk=final_pk))

    @staticmethod
    def create_database():
        DatabaseManager.create_departments()
        DatabaseManager.create_courses()
        DatabaseManager.create_companies()
        StatisticManager.create_statistics()
        UserManager.create_users()
        CAVAManager.create_CAVAs()
        InternshipManager.create_internships()

    @staticmethod
    def delete_database():
        User.objects.all().delete()
        Course.objects.all().delete()
        EngineeringDepartment.objects.all().delete()
        Company.objects.all().delete()
        EvaluationByStudent.objects.all().delete()
        Statistic.objects.all().delete()

class InternshipManager:
    @staticmethod
    def create_internships():
        cavas = CompanyApprovalValidationApplication.objects.all()
        for cava in cavas:
            if cava.status == "APPROVED":
                internship = Internship(student=cava.student, course=cava.course, company=cava.requested_company,
                                    company_approval=cava)
                internship.save()
    @staticmethod
    def list_instructors():
        for internship in Internship.objects.all():
            print("Internship name: " , internship, "Instructor name: " , internship.instructor)


class CAVAManager:
    @staticmethod
    def create_CAVAs():
        students = Student.objects.all()
        student_count = students.count()
        companies = Company.objects.all()
        companies_count = companies.count()
        for i in range(0, 8):
            number = random.randint(0, companies_count - 1)
            if i % 2 == 0:
                pk = Course.objects.all()[0].pk
            else:
                pk = Course.objects.all()[1].pk
            cava = CompanyApprovalValidationApplication(course=Course.objects.get(pk=pk),
                 file='uploads/empty.pdf', status='APPROVED', student=students[i//2],
                                                    requested_company=companies[number])
            cava.save()
        for i in range(5, student_count):
            number = random.randint(0, companies_count - 1)
            if i % 2 == 0:
                pk = Course.objects.all()[0].pk
            else:
                pk = Course.objects.all()[1].pk
            cava = CompanyApprovalValidationApplication(course=Course.objects.get(pk=pk),
                                                        file='uploads/empty.pdf', status='PENDING',
                                                        student=students[i],
                                                        requested_company=companies[number])
            cava.save()

class StatisticManager:
    @staticmethod
    def create_statistics():
        for department in EngineeringDepartment.objects.all():
            statistic = Statistic(department=department)
            statistic.save()
    @staticmethod
    def update_statistics():
        for statistic in Statistic.objects.all():
            statistic.save()

    @staticmethod
    def display_statistics():
        for statistic in Statistic.objects.all():
            print("Report grade average: ",statistic.report_grade_average )
            print("Work evaluation average: ", statistic.work_evaluation_grade_average)
            print("Company Average: ", statistic.company_evaluation_grade_average)
            print("Unsatisfactory Number: ", statistic.internship_unsatisfaction_number)
            print("Satisfactory Number: ", statistic.internship_satisfaction_number)
            print("Pending Number: ",statistic.internship_pending_number)
            print("Department Name: ", statistic.department)