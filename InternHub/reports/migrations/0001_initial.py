# Generated by Django 4.1.7 on 2023-05-26 16:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfidentialCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('RE', 'Rejected')], default='PE', max_length=2)),
                ('grade', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('company_name', models.CharField(max_length=100)),
                ('is_work_related', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('supervisor_background', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='FormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('submission_date', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstructorFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.FileField(null=True, upload_to='feedbacks/')),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('RE', 'Rejected')], default='PE', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_grade_average', models.IntegerField()),
                ('work_evaluation_grade_average', models.IntegerField()),
                ('company_evaluation_grade_average', models.IntegerField()),
                ('internship_satisfaction_number', models.IntegerField()),
                ('internship_unsatisfaction_number', models.IntegerField()),
                ('internship_pending_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(null=True, upload_to='reports/')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('file', models.FileField(null=True, upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='WorkAndReportEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_of_performing_work', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_solving_engineering_problems', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_recognizing_ethics', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_acquiring_knowledge', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_applying_knowledge', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_has_awareness', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_making_judgements', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('grade_of_preparing_reports', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('exp_is_able_to_perform_work', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_is_able_to_solve_engineering_problems', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_is_recognize_ethics', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_is_able_to_acquire_knowledge', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_is_able_to_apply_new_knowledge', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_has_awareness', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_is_make_informed_judgments', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_is_able_to_prepare_reports', models.CharField(blank=True, max_length=100, null=True)),
                ('total_work_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.task')),
            ],
            bases=('reports.task',),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.task')),
                ('status', models.CharField(choices=[('SA', 'Satisfactory'), ('RR', 'Revision Required'), ('UN', 'Unsatisfactory'), ('PE', 'Pending')], default='PE', max_length=2)),
                ('due_date', models.DateTimeField()),
            ],
            bases=('reports.task',),
        ),
    ]
