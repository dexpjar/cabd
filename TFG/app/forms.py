from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from app.models import App, User, Profile, Task, ParamsInput


# class ParamsInputForm(forms.Form):
#     class Meta:
#         model = ParamsInput
#         exclude = ()
#
#     def __init__(self, *args, **kwargs):
#         super(ParamsInput, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id='user-form'


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

        def clean(self):
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
            return self.cleaned_data

        def login(self, request):
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            return user

class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'username']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username', 'readonly':'readonly'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['institution']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Institution'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name','taskcode','state','file_input','file_output','app']

        def __init__(self, *args, **kwargs):
            super(ParamsInput, self).__init__(*args, **kwargs)
                # self.helper = FormHelper()
                # self.helper.form_id='user-form'

