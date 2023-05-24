# Generated by Django 4.1.7 on 2023-05-24 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='companyrequest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='companyapprovalvalidationapplication',
            name='course',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.course'),
        ),
        migrations.AddField(
            model_name='companyapprovalvalidationapplication',
            name='requested_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='companyapprovalvalidationapplication',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cava_applications', to='users.student'),
        ),
        migrations.AddField(
            model_name='company',
            name='departments',
            field=models.ManyToManyField(blank=True, to='users.engineeringdepartment'),
        ),
    ]
