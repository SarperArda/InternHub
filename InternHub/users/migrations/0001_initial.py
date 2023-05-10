# Generated by Django 4.1.7 on 2023-05-10 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('role', models.CharField(blank=True, choices=[('SUPERUSER', 'Superuser'), ('STUDENT', 'Student'), ('DEAN', 'Dean'), ('CHAIR', 'Chair'), ('INSTRUCTOR', 'Instructor'), ('DEPARTMENT_SECRETARY', 'Department Secretary')], max_length=50)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=50, null=True, unique=True)),
                ('user_id', models.CharField(max_length=8, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='%(class)spermissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EngineeringDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, unique=True)),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.engineeringdepartment')),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('course', models.CharField(blank=True, choices=[('CS299', 'CS299'), ('CS399', 'CS399'), ('EEE299', 'EEE299'), ('EEE399', 'EEE399'), ('ME299', 'ME299'), ('ME399', 'ME399'), ('IE299', 'IE299'), ('IE399', 'IE399')], max_length=6)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.engineeringdepartment')),
                ('grader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='users.instructor')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='DepartmentSecretary',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.engineeringdepartment')),
            ],
            options={
                'verbose_name': 'Department Secretary',
                'verbose_name_plural': 'Department Secretaries',
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Dean',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.engineeringdepartment')),
            ],
            options={
                'verbose_name': 'Dean',
                'verbose_name_plural': 'Deans',
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Chair',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.engineeringdepartment')),
            ],
            options={
                'verbose_name': 'Chair',
                'verbose_name_plural': 'Chairs',
            },
            bases=('users.user',),
        ),
    ]
