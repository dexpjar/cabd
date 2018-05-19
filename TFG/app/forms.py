from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from app.models import App, User, Profile, Task, ParamsInput, ImageSlideshow, MyCompany, Section


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

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'is_superuser', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),
            'is_superuser': forms.CheckboxInput(),
            'is_active': forms.CheckboxInput(),
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

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['taskcode','name','citation', 'image','command','description']
        widgets = {
            'taskcode': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Taskcode'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'citation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citation'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'command': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Command'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

class MyCompanyForm(forms.ModelForm):
    class Meta:
        model = MyCompany
        fields = ['logo','name','address', 'phone','email','citations']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'citations': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citations'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name','taskcode','state','file_input','file_output','app']

        def __init__(self, *args, **kwargs):
            super(ParamsInput, self).__init__(*args, **kwargs)

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name','state','file_input','file_output','app','user','taskcode']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'file_input': forms.FileInput(attrs={'class': 'form-control'}),
            'file_output': forms.FileInput(attrs={'class': 'form-control'}),
            'taskcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Taskcode'}),
        }


class ImageSlideshowForm(forms.ModelForm):
    class Meta:
        model = ImageSlideshow
        fields = ['image']


class ParamForm(forms.ModelForm):
    LIST_INPUT = (('text', 'Text'), ('file', 'File'), ('read', 'Read'))
    state = forms.ChoiceField(choices=LIST_INPUT)
    class Meta:
        model = ParamsInput
        fields = ['name','option','value','allowed_format','is_required','is_file_input','is_file_output','app','state','info']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'option': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option'}),
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Value'}),
            'allowed_format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Allowed Format'}),
            'is_required': forms.CheckboxInput(),
            'is_file_input': forms.CheckboxInput(),
            'is_file_output': forms.CheckboxInput(),
            'info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Info'}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title','description','app']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Title'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

