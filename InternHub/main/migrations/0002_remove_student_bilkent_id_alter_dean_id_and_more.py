# Generated by Django 4.1.7 on 2023-05-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='bilkent_id',
        ),
        migrations.AlterField(
            model_name='dean',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='departmentsecretary',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='superuser',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]
