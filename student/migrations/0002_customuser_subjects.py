# Generated by Django 5.0.4 on 2024-04-25 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subjects',
            field=models.ManyToManyField(related_name='students', to='student.subject', verbose_name='Subjects'),
        ),
    ]