from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Faculty(models.Model):
    name = models.CharField(verbose_name=_("Faculty name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')


class Subject(models.Model):
    lecturers = models.ManyToManyField('Lecture', related_name='subjects')
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_("Subject Name"))
    description = models.TextField(verbose_name=_("Subject Description"))
    syllabus = models.FileField(upload_to='syllabus/', verbose_name=_("Syllabus"))
    faculties = models.ManyToManyField(Faculty, related_name='subjects')
    # lecturers = models.ManyToManyField('Lecture', related_name='subjects')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')


class Lecture(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Lecture Name"))
    surname = models.CharField(max_length=255, verbose_name=_("Lecture Surname"))

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = _('Lecture')
        verbose_name_plural = _('Lectures')


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students', verbose_name=_('Faculty'),
                                null=True, blank=True)
    subjects = models.ManyToManyField(Subject, verbose_name=_('Subjects'))
    name = models.CharField(max_length=255, verbose_name=_("Student Name"))
    surname = models.CharField(max_length=255, verbose_name=_("Student Surname"))
    # faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students', verbose_name=_('Faculty'),
    #                             null=True, blank=True)
    # subjects = models.ManyToManyField(Subject, verbose_name=_('Subjects'))

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
