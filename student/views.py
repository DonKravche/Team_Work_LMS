from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, TaskForm, AssignmentForm, AttendanceForm
from .models import Student, Subject, Task, Assignment, Attendance, CustomUser, Lecture
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


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
            if user.is_student:
                return redirect('students_base')
            elif user.is_lecturer:
                return redirect('lecturers_page')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def students_base(request):
    task = Task.objects.first()
    context = {'task_id': task.id}
    return render(request, 'students_base.html', context)


@login_required
def lecturers_page(request):
    if request.user.is_authenticated:
        # User is a lecturer
        lecturer = request.user

        try:
            # lecture = Lecture.objects.get(name=lecturer.username)
            # subjects = Subject.objects.filter(lecturers=lecture)
            return render(request, 'lecturers_page.html', {'user': lecturer})
        except ObjectDoesNotExist:
            message = "You are not associated with any lecture."
            return render(request, 'lecturers_page.html', {'user': lecturer, 'message': message})
    else:
        return redirect('home')


def students_page(request):
    student = Student.objects.get(user=request.user)
    faculty_subjects = student.faculty.subjects.all()

    if request.method == 'POST':
        selected_subjects_ids = request.POST.getlist('students_page')
        if len(selected_subjects_ids) < 2 or len(selected_subjects_ids) > 7:
            return render(request, 'students_page.html', {'message': 'Please select at least 2 & max 7 subjects.',
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


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.lecturer = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('create_task')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})


def submit_assignment(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.task = task
            assignment.save()
            messages.success(request, 'Assignment submitted successfully.')
            return redirect('submit_assignment', task_id=task_id)
    else:
        form = AssignmentForm()
    return render(request, 'submit_assignment.html', {'form': form, 'task': task})


def record_attendance(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    students = CustomUser.objects.filter(student_profile__subjects=subject)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.subject = subject
            attendance.save()
            form.save_m2m()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('record_attendance', subject_id=subject_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

    else:
        form = AttendanceForm()

    return render(request, 'record_attendance.html', {'form': form, 'subject': subject, 'students': students})
