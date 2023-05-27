from django.contrib.auth.base_user import BaseUserManager
from users.models import User, Student, Instructor, DepartmentSecretary, Chair, Dean
from users.models import Course, EngineeringDepartment
from company.models import Company, CompanyApprovalValidationApplication,EvaluationByStudent
from reports.models import Internship
import json
from users.models import RoleMixin
from django.contrib.auth.hashers import make_password
import random
from users.models import UserManager

class DatabaseManager():

    @staticmethod
    def restart_database():
        User.objects.all().delete()
        Course.objects.all().delete()
        EngineeringDepartment.objects.all().delete()
        Company.objects.all().delete()
        EvaluationByStudent.objects.all().delete()
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
                company = Company(**company_data['fields'])
                company.save()

    @staticmethod
    def create_database():
        DatabaseManager.create_departments()
        DatabaseManager.create_courses()
        DatabaseManager.create_companies()
        UserManager.create_users()
        CAVAManager.create_CAVAs()
        InternshipManager.create_internships()

class InternshipManager:
    @staticmethod
    def create_internships():
        cavas = CompanyApprovalValidationApplication.objects.all()
        for cava in cavas:
            internship = Internship(student=cava.student, course=cava.course, company=cava.requested_company,
                                    company_approval=cava)
            internship.save()
    @staticmethod
    def list_instructors():
        for internship in Internship.objects.all():
            print("Internship name: " , internship, "Instructor name: " , internship.instructor)

class UserManager(BaseUserManager):

    def create_user(self, user_id, password=None, email=None, first_name=None, last_name=None):
        if not user_id:
            raise ValueError('Users must have a valid id')

        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None):
        user = self.create_user(
            user_id=user_id,
            password=password,
        )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.role = RoleMixin.Role.SUPERUSER
        user.save(using=self._db)
        return user

    @staticmethod
    def create_instructors():
        with open('fixtures/instructors.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = user['fields']['department']
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                instructor = Instructor(**user['fields'], password=hashed_password)
                instructor.save()
    @staticmethod
    def create_students():
        with open('fixtures/students.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = user['fields']['department']
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                student = Student(**user['fields'], password=hashed_password)
                student.save()

    @staticmethod
    def create_department_secretaries():
        with open('fixtures/secretary.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = user['fields']['department']
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                ds = DepartmentSecretary(**user['fields'], password=hashed_password)
                ds.save()

    @staticmethod
    def create_dean():
        with open('fixtures/dean.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = user['fields']['department']
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                dean = Dean(**user['fields'], password=hashed_password)
                dean.save()

    @staticmethod
    def create_chairs():
        with open('fixtures/chairs.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = user['fields']['department']
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                chair = Chair(**user['fields'], password=hashed_password)
                chair.save()

    @staticmethod
    def create_supers():
        with open('fixtures/superuser.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = user['fields']['department']
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                super_user = User(**user['fields'], password=hashed_password)
                super_user.role = RoleMixin.Role.SUPERUSER
                super_user.save()
    @staticmethod
    def create_users():
        UserManager.create_instructors()
        UserManager.create_dean()
        UserManager.create_students()
        UserManager.create_department_secretaries()
        UserManager.create_supers()
        UserManager.create_chairs()

class CAVAManager:
    @staticmethod
    def create_CAVAs():
        students = Student.objects.all()
        student_count = students.count()
        companies = Company.objects.all()
        companies_count = companies.count()
        for i in range(0, student_count):
            number = random.randint(0, companies_count - 1)
            if i % 2 == 0:
                pk = 1
            else:
                pk = 2
            cava = CompanyApprovalValidationApplication(course=Course.objects.get(pk=pk),
                 file='uploads/empty.pdf', status='APPROVED', student=students[i//2 + student_count//2],
                                                    requested_company=companies[number])
            print(students[i//2].first_name + students[i//2].last_name)
            cava.save()