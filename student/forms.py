from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from student.models import Faculty, Student


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    surname = forms.CharField(max_length=255, required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'surname', 'faculty']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.save()

        student = Student.objects.create(user=user, faculty=self.cleaned_data['faculty'])
        student.save()

        return user


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'