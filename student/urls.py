from django.urls import path

from student import views
from student.views import home

urlpatterns = [
    path('home/', home, name='home'),
]