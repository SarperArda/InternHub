# Generated by Django 4.1.7 on 2023-05-10 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_student_assigned_instructor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='students',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.instructor'),
        ),
    ]
