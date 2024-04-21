# Generated by Django 5.0.4 on 2024-04-21 19:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Faculty name')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Lecture Name')),
                ('surname', models.CharField(max_length=255, verbose_name='Lecture Surname')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Subject Name')),
                ('description', models.TextField(verbose_name='Subject Description')),
                ('syllabus', models.FileField(upload_to='syllabi/', verbose_name='Syllabus')),
                ('faculties', models.ManyToManyField(related_name='subjects', to='student.faculty')),
                ('lecturers', models.ManyToManyField(related_name='subjects', to='student.lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Student Name')),
                ('surname', models.CharField(max_length=255, verbose_name='Student Surname')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='student.faculty', verbose_name='faculty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
                ('subjects', models.ManyToManyField(to='student.subject', verbose_name='subjects')),
            ],
        ),
    ]
