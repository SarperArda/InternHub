# Generated by Django 4.1 on 2023-05-26 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("company", "0002_initial"),
        ("users", "0001_initial"),
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="statistic",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="statistic",
                to="users.engineeringdepartment",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="company",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="company.company",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="company_approval",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="company.companyapprovalvalidationapplication",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="company_evaluation",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="company.evaluationbystudent",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="confidential_company_form",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="reports.confidentialcompany",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="users.course",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="instructor",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="users.instructor",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="student",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="internship",
                to="users.student",
            ),
        ),
        migrations.AddField(
            model_name="internship",
            name="work_and_report_evaluation_form",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="internship",
                to="reports.workandreportevaluation",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="internship",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to="reports.internship",
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="submission_field",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedback",
                to="reports.submission",
            ),
        ),
    ]
