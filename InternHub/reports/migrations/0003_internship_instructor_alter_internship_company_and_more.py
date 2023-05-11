# Generated by Django 4.1.7 on 2023-05-10 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_student_course_remove_student_students'),
        ('company', '0003_alter_companyrelateddemand_company_and_more'),
        ('reports', '0002_confidentialcompanyform_status_gradingform_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='users.instructor'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='company.company'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='company_approval',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='company.companyapprovalvalidationapplication'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='company_evaluation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='company.evaluationbystudent'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='confidential_company_form',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='reports.confidentialcompanyform'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='evaluation_form',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='reports.evaluationform'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='grading_form',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internship', to='reports.gradingform'),
        ),
    ]
