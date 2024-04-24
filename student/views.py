from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from student.forms import UserRegistrationForm, UserLoginForm
from student.models import Student, Subject


def home(request):
    return render(request, 'home.html')


def login_user(request):
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
    student = request.user.student
    faculty_subjects = student.faculty.subjects.all()

    if request.method == 'POST':
        selected_subjects_ids = request.POST.getlist('students_page')
        if len(selected_subjects_ids) < 3 or len(selected_subjects_ids) > 7:
            return render(request, 'students_page.html', {'message': 'Please select at least 3 & max 7 subjects.',
                                                          'faculty_subjects': faculty_subjects}, )
        else:
            selected_subjects = Subject.objects.filter(pk__in=selected_subjects_ids)
            student.subjects.set(selected_subjects)
            return render(request, 'answer.html', {'user': request.user, 'selected_subjects': selected_subjects})
    else:
        context = {
            'user': request.user,
            'faculty_subjects': faculty_subjects
        }
        return render(request, 'students_page.html', context)


def logout_(request):
    logout(request)
    return redirect('home')
