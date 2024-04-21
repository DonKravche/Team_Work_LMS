from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm
from .models import Student, Subject
from django.db import IntegrityError


def home(request):
    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login_')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration_form.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            student = user.student
            return redirect('students_page')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def students_page(request):
    if request.method == 'POST':
        student = request.user.student
        faculty_subjects = student.faculty.subjects.all()
        selected_subjects = request.POST.getlist('students_page')
        if len(selected_subjects) < 3 or len(selected_subjects) > 7:
            return HttpResponseBadRequest("You must choose between 3 and 7 subjects.")
        else:
            selected_subjects = Subject.objects.filter(pk__in=selected_subjects)
            student.subjects.set(selected_subjects)
            return render(request, 'answer.html', {'user': request.user, 'faculty_subjects': faculty_subjects})
    else:
        student = request.user.student
        faculty_subjects = student.faculty.subjects.all()
        context = {
            'user': request.user,
            'faculty_subjects': faculty_subjects
        }
        return render(request, 'students_page.html', context)
