# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-23 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsil', '0002_auto_20170617_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='partner',
            field=models.ManyToManyField(to='wsil.CoursePartner'),
        ),
        migrations.AlterField(
            model_name='coursepartner',
            name='course_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='coursepartner',
            name='partner_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='features',
            name='ajax',
            field=models.CharField(help_text='AJAX', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='caching_framework',
            field=models.CharField(help_text='Caching Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='db_migration_framework',
            field=models.CharField(help_text='DB Migration Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='form_validation_framework',
            field=models.CharField(help_text='Form Validation Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='library_framework_name',
            field=models.CharField(help_text='Library or Framework name', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='localization',
            field=models.CharField(help_text='Localization', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='mvc_framework',
            field=models.CharField(help_text='MVC Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='mvc_push_pull',
            field=models.CharField(help_text='MVC Push Pull', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='orm',
            field=models.CharField(help_text='ORM', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='security_framework',
            field=models.CharField(help_text='Security Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='template_framework',
            field=models.CharField(help_text='Template Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='testing_framework',
            field=models.CharField(help_text='Testing Framework', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
