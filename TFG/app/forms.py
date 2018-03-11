from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from app.models import App, User, Profile


# class UserForm(forms.Form):
#     email = forms.CharField(label='Email',required=True)
#     password = forms.CharField(label='Password', required=True)
#     name = forms.CharField(required=True)
#     surname = forms.CharField(required=True)

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         exclude = ()
#
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id='user-form'
#
#     def clean_name(self):
#         email = self.cleaned_data['email']
#         if email == '':
#             raise ValidationError("")
#         return email
#
#     def clean(self):
#         cleaned_data = super(UserForm, self).clean()
#         name = self.cleaned_data.get('name')

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        # widgets = {
        #     'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),
        #     'username': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
        # }

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
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),
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

