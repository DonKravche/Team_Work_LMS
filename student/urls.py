from django.urls import path

from student import views
from student.views import register

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', register, name='register_student'),
    path('login/', views.login_, name='login_'),
    path('students_page/', views.students_page, name='students_page'),
    path('logout/', views.logout_, name='logout_'),
    path('create-task/', views.create_task, name='create_task'),
    path('submit-assignment/<int:task_id>/', views.submit_assignment, name='submit_assignment'),
    path('record-attendance/<int:subject_id>/', views.record_attendance, name='record_attendance'),
    path('lecturers_page/', views.lecturers_page, name='lecturers_page'),
    path('students_base', views.students_base, name='students_base'),
    path('submitted_assignments/', views.submitted_assignments, name='submitted_assignments'),
]
