# Generated by Django 3.2.15 on 2022-09-28 13:49

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=150, unique=True, verbose_name='user name')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('about', models.TextField(blank=True, max_length=500, verbose_name='about')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='phone number')),
                ('postcode', models.CharField(blank=True, max_length=12, verbose_name='postcode')),
                ('address_line_1', models.CharField(blank=True, max_length=150, verbose_name='address line one')),
                ('address_line_2', models.CharField(blank=True, max_length=150, verbose_name='address line two')),
                ('town_city', models.CharField(blank=True, max_length=150, verbose_name='city')),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Accounts',
                'verbose_name_plural': 'Accounts',
            },
        ),
    ]