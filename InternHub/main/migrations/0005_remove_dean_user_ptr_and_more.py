# Generated by Django 4.1 on 2023-05-08 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_student_course_alter_user_email_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="dean", name="user_ptr",),
        migrations.RemoveField(model_name="departmentsecretary", name="user_ptr",),
        migrations.RemoveField(model_name="instructor", name="user_ptr",),
        migrations.RemoveField(model_name="student", name="user_ptr",),
        migrations.DeleteModel(name="Chair",),
        migrations.DeleteModel(name="Dean",),
        migrations.DeleteModel(name="DepartmentSecretary",),
        migrations.DeleteModel(name="Instructor",),
        migrations.DeleteModel(name="Student",),
    ]
