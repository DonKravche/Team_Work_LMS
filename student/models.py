from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    subjects = models.ManyToManyField('Subject', related_name='students',
                                      verbose_name=_('Subjects'))

    def __str__(self):
        return self.username


class Faculty(models.Model):
    name = models.CharField(verbose_name=_("Faculty name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='student_profile')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students', verbose_name=_('Faculty'),
                                null=True, blank=True)
    subjects = models.ManyToManyField('Subject', verbose_name=_('Subjects'))
    name = models.CharField(max_length=255, verbose_name=_("Student Name"))
    surname = models.CharField(max_length=255, verbose_name=_("Student Surname"))

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')


class Task(models.Model):
    lecturer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tasks',
                                 verbose_name=_("Lecturer"))
    description = models.TextField(verbose_name=_("Task Description"))
    execution_date = models.DateField(verbose_name=_("Execution Date"))

    def __str__(self):
        return self.description


class Assignment(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='assignments',
                                verbose_name=_("Student"))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments', verbose_name=_("Task"))
    description = models.TextField(verbose_name=_("Assignment Description"))
    attached_file = models.FileField(upload_to='assignments/', verbose_name=_("Attached File"))

    def __str__(self):
        return self.description


class Attendance(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='attendances',
                                verbose_name=_("Subject"))
    students = models.ManyToManyField(get_user_model(), related_name='attendances', blank=True,
                                      verbose_name=_("Students"))
    date = models.DateField(verbose_name=_("Attendance Date"))

    def __str__(self):
        return f"{self.subject} - {self.date}"


class Subject(models.Model):
    lecturers = models.ManyToManyField('Lecture', related_name='subjects')
    title = models.CharField(max_length=255, verbose_name=_("Subject Name"))
    description = models.TextField(verbose_name=_("Subject Description"))
    syllabus = models.FileField(upload_to='syllabus/', verbose_name=_("Syllabus"))
    faculties = models.ManyToManyField(Faculty, related_name='subjects')

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
