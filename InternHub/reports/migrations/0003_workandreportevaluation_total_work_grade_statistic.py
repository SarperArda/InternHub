# Generated by Django 4.1 on 2023-05-26 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        ("reports", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="workandreportevaluation",
            name="total_work_grade",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Statistic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("report_grade_average", models.FloatField()),
                ("work_evaluation_grade_average", models.FloatField()),
                ("company_evaluation_grade_average", models.FloatField()),
                ("internship_satisfaction_number", models.IntegerField()),
                ("internship_unsatisfaction_number", models.IntegerField()),
                ("internship_pending_number", models.IntegerField()),
                (
                    "department",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statistic",
                        to="users.engineeringdepartment",
                    ),
                ),
            ],
        ),
    ]
