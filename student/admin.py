from django.contrib import admin

# Register your models here.

from django.contrib import admin

from student.models import Student, Faculty, Subject, Lecture


# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'faculty')
    search_fields = ('name', 'surname', 'faculty__name')
    list_filter = ('faculty',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Wrap the field name in a tuple


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Wrap the field name in a tuple


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
