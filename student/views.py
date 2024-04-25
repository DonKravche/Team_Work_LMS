from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm, TaskForm, SubmissionForm
from .models import Student, Subject

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task, Submission, Attendance
from .forms import TaskForm, SubmissionForm


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


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_create.html', {'form': form})


@login_required
def submit_assignment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.save()
            return redirect('task_list')
    else:
        form = SubmissionForm()
    return render(request, 'submission_form.html', {'form': form, 'task': task})


@login_required
def record_attendance(request, subject):
    if request.method == 'POST':
        date = request.POST.get('date')
        student_ids = request.POST.getlist('students')
        attendance = Attendance(subject=subject, date=date)
        attendance.save()
        attendance.students.set(student_ids)
        return redirect('attendance_list')
    else:
        students = User.objects.all()
    return render(request, 'attendance.html', {'students': students, 'subject': subject})
