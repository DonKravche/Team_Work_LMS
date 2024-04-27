from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from student.forms import UserRegistrationForm, UserLoginForm, TaskForm, AssignmentForm, AttendanceForm
from student.models import Student, Subject, Task, Assignment, Attendance, CustomUser, Lecturer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from .models import Task, Assignment


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
    if task:  # Check if task is not None
        context = {'task_id': task.id}
        return render(request, 'students_base.html', context)
    else:
        # Handle the case where no Task objects exist
        context = {'message': 'No tasks available.'}
        return render(request, 'students_base.html', context)


# @login_required
# def lecturers_page(request):
#     if request.user.is_authenticated:
#         # User is a lecturer
#         lecturer = request.user.lecturer  # get the lecturer object
#
#         try:
#             subjects = Subject.objects.filter(lecturers=lecturer)
#             return render(request, 'lecturers_page.html', {'user': request.user, 'subjects': subjects})
#         except Subject.DoesNotExist:
#             message = "You are not associated with any Subject."
#             return render(request, 'lecturers_page.html', {'user': request.user, 'message': message})
#     else:
#         return redirect('home')

@login_required
def lecturers_page(request):
    if request.user.is_authenticated:
        # User is a lecturer
        if hasattr(request.user, 'lecturer'):
            lecturer = request.user.lecturer  # get the lecturer object

            try:
                subjects = Subject.objects.filter(lecturers=lecturer)
                return render(request, 'lecturers_page.html', {'user': request.user, 'subjects': subjects})
            except Subject.DoesNotExist:
                message = "You are not associated with any Subject."
                return render(request, 'lecturers_page.html', {'user': request.user, 'message': message})
        else:
            # Handle the case where the user doesn't have a related Lecturer instance
            message = "You are not a lecturer."
            return render(request, 'lecturers_page.html', {'user': request.user, 'message': message})
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
            print(selected_subjects)
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


# @login_required
# def submitted_assignments(request):
#     if request.user.is_authenticated and hasattr(request.user, 'lecturer'):
#         lecturer = request.user.lecturer
#         subjects = Subject.objects.filter(lecturers=lecturer)
#         tasks = Task.objects.filter(subject__in=subjects)
#         assignments = Assignment.objects.filter(task__in=tasks)
#         return render(request, 'submitted_assignments.html', {'assignments': assignments})
#     else:
#         return redirect('home')


# @login_required
# def submitted_assignments(request):
#     if hasattr(request.user, 'lecturer'):
#         tasks = Task.objects.filter(lecturer=request.user)
#         assignments = Assignment.objects.filter(task__in=tasks)
#         print(assignments)
#         return render(request, 'submitted_assignments.html', {'assignments': assignments})
#     else:
#         return redirect('home')


@login_required
def submitted_assignments(request):
    if hasattr(request.user, 'lecturer'):
        lecturer = Lecturer.objects.get(user=request.user)
        tasks = Task.objects.filter(lecturer=request.user)
        assignments = Assignment.objects.filter(task__in=tasks)
        return render(request, 'submitted_assignments.html', {'assignments': assignments})
    elif hasattr(request.user, 'student'):
        student = Student.objects.get(user=request.user)
        assignments = Assignment.objects.filter(student=student)
        return render(request, 'submitted_assignments.html', {'assignments': assignments})
    else:
        return redirect('home')
