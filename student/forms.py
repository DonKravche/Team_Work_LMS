from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from student.models import Task, Assignment, Attendance, CustomUser, Faculty, Student


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    surname = forms.CharField(max_length=255, required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'name', 'surname', 'faculty']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.is_student = True
        user.save()

        student = Student.objects.create(user=user, faculty=self.cleaned_data['faculty'])
        student.save()

        return user


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'


class TaskForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)
    title = forms.CharField(max_length=255, required=True)
    subject = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Task
        fields = ['description', 'execution_date', 'faculty', 'title', 'subject']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['description', 'attached_file', 'submission_date']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'students']
