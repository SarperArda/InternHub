# Generated by Django 4.1.7 on 2023-05-10 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('field', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyRelatedDemand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='uploads/')),
                ('demand_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyApprovalValidationApplication',
            fields=[
                ('companyrelateddemand_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='company.companyrelateddemand')),
            ],
            bases=('company.companyrelateddemand',),
        ),
        migrations.CreateModel(
            name='CompanyRequest',
            fields=[
                ('companyrelateddemand_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='company.companyrelateddemand')),
            ],
            bases=('company.companyrelateddemand',),
        ),
        migrations.CreateModel(
            name='EvaluationByStudent',
            fields=[
                ('companyrelateddemand_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='company.companyrelateddemand')),
                ('grade', models.IntegerField(null=True)),
            ],
            bases=('company.companyrelateddemand',),
        ),
    ]
