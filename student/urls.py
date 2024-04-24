from django.urls import path

from student import views
from student.views import register

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', register, name='register_student'),
    path('login/', views.login_, name='login_'),
    path('students_page/', views.students_page, name='students_page'),
    path('logout/', views.logout_, name='logout_'),
]