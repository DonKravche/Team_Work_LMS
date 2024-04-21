from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=255, verbose_name="Faculty name")

    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Subject Name")
    description = models.TextField(verbose_name="Subject Description")
    syllabus = models.FileField(upload_to='syllabi/', verbose_name="Syllabus")
    faculties = models.ManyToManyField(Faculty, related_name='subjects')
    lecturers = models.ManyToManyField('Lecture', related_name='subjects')

    def __str__(self):
        return self.title


class Lecture(models.Model):
    name = models.CharField(max_length=255, verbose_name="Lecture Name")
    surname = models.CharField(max_length=255, verbose_name="Lecture Surname")

    def __str__(self):
        return f"{self.name} {self.surname}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=255, verbose_name="Student Name")
    surname = models.CharField(max_length=255, verbose_name="Student Surname")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students', verbose_name='faculty',
                                null=True, blank=True)
    subjects = models.ManyToManyField(Subject, verbose_name='subjects')

    def __str__(self):
        return f"{self.name} {self.surname}"