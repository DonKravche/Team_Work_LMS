from student.models import Student, Faculty, Subject, Lecturer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from student.models import CustomUser


class SubjectInline(admin.TabularInline):
    model = CustomUser.subjects.through
    verbose_name = "Subject"
    verbose_name_plural = "Subjects"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_student', 'is_lecturer']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_student', 'is_lecturer')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_lecturer'),
        }),
    )
    inlines = [SubjectInline]


admin.site.register(CustomUser, CustomUserAdmin)


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


@admin.register(Lecturer)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
