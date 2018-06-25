# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import choice

import timestamp as timestamp
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Q
from django import forms
from django.forms.utils import ErrorList
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import HttpResponse

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, FormView
from pexpect import pxssh

from app.forms import RegisterForm, ProfileForm, EditForm, LoginForm, TaskForm, ImageSlideshowForm, UserForm, AppForm, \
    MyCompanyForm, SectionForm, TaskAdminForm, ParamForm, ParamFileForm, ParamTextForm, ParamOptionForm, \
    ParamSelectForm, AppDetailForm, UserPasswordForm
from app.models import App, User, Profile, Task, Section, MyCompany, ImageSlideshow, ParamsInput, ParamsInputFile, \
    ParamsInputText, ParamsInputSelect, ParamInputOption, Compatibility
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse_lazy
from django.utils import six

import paramiko
import os
from datetime import datetime, timedelta

# Funcion que comprueba que los campos del registro son validos y crea el usuario
def create_user_view(request):
    if request.method == 'POST':
        register = RegisterForm(request.POST, prefix='register')
        usrprofile = ProfileForm(request.POST, prefix='profile')
        if register.is_valid() and usrprofile.is_valid():
            user = register.save()
            user.set_password(register.cleaned_data['password'])
            user.is_active = False
            user.save()
            usrprof = usrprofile.save(commit=False)
            usrprof.user = user
            usrprof.subscribed = '1'
            usrprof.save()
            company_name = MyCompany.objects.all()[:1].get()
            asunto = "Account New " + user.email
            mensaje = "The user with email: " + user.email + "is trying to login, you have to active this account through the admin panel"
            mail = EmailMessage(asunto, mensaje, to=['daniel.tfg.cabd@gmail.com'])
            mail.send()
            return redirect('login')
        else:
            userform = RegisterForm(prefix='register')
            userprofileform = ProfileForm(prefix='profile')
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, 'register.html',
                          {'company_name': company_name, 'userform': userform, 'userprofileform': userprofileform})
    else:
        userform = RegisterForm(prefix='register')
        userprofileform = ProfileForm(prefix='profile')
        company_name = MyCompany.objects.all()[:1].get()
        return render(request, 'register.html',
                      {'company_name': company_name, 'userform': userform, 'userprofileform': userprofileform})


class Login(FormView):
    # Establecemos la plantilla a utilizar
    template_name = 'index.html'
    # Le indicamos que el formulario a utilizar es el formulario de autenticación de Django
    form_class = AuthenticationForm
    form_class.base_fields['username'].widget.attrs['class'] = "form-control"
    form_class.base_fields['password'].widget.attrs['class'] = "form-control"
    form_class.company_name = MyCompany.objects.all()[:1].get()
    form_class.first_slideshow = ImageSlideshow.objects.all()[:1].get()
    form_class.slideshows = ImageSlideshow.objects.all()[1:]
    form_class.apps = App.objects.all()
    # Le decimos que cuando se haya completado exitosamente la operación nos redireccione a la url bienvenida de la aplicación personas
    success_url = reverse_lazy("principal:list-apps-view")

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario está autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        # Sino lo está entonces nos muestra la plantilla del login simplemente
        else:
            company = MyCompany.objects.all()[:1].get()
            company_name = company.name
            args = company_name
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


class AdminLogin(FormView):
    model = User
    form_class = AuthenticationForm
    template_name = "index_admin.html"
    success_url = reverse_lazy("principal:admin-view")

    def dispatch(self, request, *args, **kwargs):
        company = MyCompany.objects.all()[:1].get()
        company_name = company.name
        args = company_name
        return super(AdminLogin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = self.request.POST['username']
        user = self.model.objects.get(username=username)
        if not user.is_superuser:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                u'This user is not superuser'
            ])
            return super(AdminLogin, self).form_invalid(form)
        else:
            login(self.request, form.get_user())
            return super(AdminLogin, self).form_valid(form)

#Menu Index : Contact, Getting Started

def contact_view(request):
    company_name = MyCompany.objects.all()[:1].get()
    context = {
        'company_name': company_name,
    }
    return render(request, 'contact.html', context)

def getting_started_view(request):
    company_name = MyCompany.objects.all()[:1].get()
    context = {
        'company_name': company_name,
    }
    return render(request, 'getting_started.html', context)

def citations_view(request):
    company_name = MyCompany.objects.all()[:1].get()
    context = {
        'company_name': company_name,
    }
    return render(request, 'citations.html', context)

@login_required
def detail_app_view(request, pk):
    apps = App.objects.all()
    app_select = App.objects.get(pk=pk)
    sections = Section.objects.filter(app=app_select)
    company_name = MyCompany.objects.all()[:1].get()
    current_user = request.user
    try:
        tasks = Task.objects.filter(Q(user=current_user) & Q(app=app_select))
    except Task.DoesNotExist:
        tasks = None
    context = {
        'apps': apps,
        'app_select': app_select,
        'sections': sections,
        'company_name': company_name,
        'tasks': tasks,
    }
    return render(request, 'app_detail.html', context)


@login_required
def admin_view(request):
    user_count = User.objects.count()
    app_count = App.objects.count()
    mycompany_count = MyCompany.objects.count()
    task_count = Task.objects.count()
    image_count = ImageSlideshow.objects.count()
    param_file_count = ParamsInputFile.objects.count()
    param_text_count = ParamsInputText.objects.count()
    param_select_count = ParamsInputSelect.objects.count()
    param_option_count = ParamInputOption.objects.count()
    param_count = param_file_count + param_text_count + param_select_count + param_option_count
    section_count = Section.objects.count()
    company_name = MyCompany.objects.all()[:1].get()
    # current_user = request.user
    context = {
        'user_count': user_count,
        'app_count': app_count,
        'mycompany_count': mycompany_count,
        'task_count': task_count,
        'image_count': image_count,
        'param_count': param_count,
        'section_count': section_count,
        'company_name': company_name,
    }
    return render(request, 'dashboard_admin.html', context)


@login_required
def tasks_app_view(request, pk):
    apps = App.objects.all()
    app_select = App.objects.get(pk=pk)
    company_name = MyCompany.objects.all()[:1].get()
    current_user = request.user
    try:
        tasks = Task.objects.filter(Q(user=current_user) & Q(app=app_select))
    except Task.DoesNotExist:
        tasks = None
    context = {
        'apps': apps,
        'app_select': app_select,
        'company_name': company_name,
        'tasks': tasks,
    }
    return render(request, 'app_tasks.html', context)


class AppListView(LoginRequiredMixin, View):
    def get(self, request):
        apps = App.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        try:
            tasks = Task.objects.filter(user=current_user)
        except Task.DoesNotExist:
            tasks = None
        return render(request, "dashboard.html",
                      {'apps': apps, 'user': current_user, 'tasks': tasks, 'company_name': company_name})


class AppFormView(LoginRequiredMixin, View):
    model = Task
    form_class = TaskForm

    def get(self, request, pk):
        apps = App.objects.all()
        app_select = App.objects.get(pk=pk)
        taskform = self.form_class()
        params_file = ParamsInputFile.objects.filter(app_id=pk)
        params_text = ParamsInputText.objects.filter(app_id=pk)
        params_select = ParamsInputSelect.objects.filter(app_id=pk)
        params_option = {}
        for select in params_select:
            options = ParamInputOption.objects.filter(select_id=select.pk)
            params_option[select] = options
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        try:
            tasks = Task.objects.filter(user=current_user)
        except Task.DoesNotExist:
            tasks = None
        context = {
            'apps': apps,
            'user': current_user,
            'tasks': tasks,
            'company_name': company_name,
            'app_select': app_select,
            'params_file': params_file,
            'params_text': params_text,
            'params_select': params_select,
            'params_option': params_option,
            'taskform': taskform,
        }
        return render(request, "form_app.html", context)


class TaskDetailView(LoginRequiredMixin, View):
    model = App
    form_class = AppDetailForm

    def get(self, request, pk):
        apps = App.objects.all()
        task_select = Task.objects.get(pk=pk)
        app_task = App.objects.get(pk=task_select.app.pk)
        compatibility = app_task.app_compatibility.all()
        # appform = self.form_class(instance=compatibility)
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        context = {
            'apps': apps,
            'user': current_user,
            'task_select': task_select,
            'company_name': company_name,
            'compatibility': compatibility,
        }
        return render(request, "form_task.html", context)

class SendAppCompatibilityView(LoginRequiredMixin, View):
    model = Task
    form_class = TaskForm

    def post(self, request, pk):
        apps = App.objects.all()
        task_select = Task.objects.get(pk=pk)
        app = task_select.app
        taskform = self.form_class()
        params_file = ParamsInputFile.objects.filter(app_id=app)
        params_text = ParamsInputText.objects.filter(app_id=app)
        params_select = ParamsInputSelect.objects.filter(app_id=app)
        params_option = {}
        for select in params_select:
            options = ParamInputOption.objects.filter(select_id=select.pk)
            params_option[select] = options
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        try:
            tasks = Task.objects.filter(user=current_user)
        except Task.DoesNotExist:
            tasks = None
        context = {
            'apps': apps,
            'user': current_user,
            'tasks': tasks,
            'company_name': company_name,
            'app_select': app,
            'params_file': params_file,
            'params_text': params_text,
            'params_select': params_select,
            'file_input_compatibility': task_select.file_input,
            'params_option': params_option,
            'taskform': taskform,
        }
        return render(request, "form_app_compatibility.html", context)

# Crear Tarea

def create_task_view(request, pk):
    if request.method == 'POST':
        taskform = TaskForm(request.POST, request.FILES)
        tasknew = taskform.save()
        app_select = App.objects.get(pk=pk)
        tasknew.app = app_select
        command = app_select.command
        taskcode = app_select.taskcode
        current_user = request.user
        for valor in request.POST:
            if valor != 'csrfmiddlewaretoken' and valor != 'file_input_option' and valor != 'file_output_option' and valor!= 'file_allowed_input' and valor!= 'file_allowed_output':
                if request.POST[valor]:
                    command += " " + valor + " " + request.POST[valor]
                else:
                    command += " " + valor
        if 'file_input_option' in request.POST:
            param_file_input = ParamsInputFile.objects.get(app_id=app_select.pk, type='input')
            list_input = param_file_input.allowed_format.split(',')
            encontrado=False
            for input in list_input:
                if request.FILES['file_input'].name.endswith(str(input)):
                    encontrado = True
            if not encontrado:
                apps = App.objects.all()
                app_select = App.objects.get(pk=pk)
                taskform = TaskForm()
                params_file = ParamsInputFile.objects.filter(app_id=pk)
                params_text = ParamsInputText.objects.filter(app_id=pk)
                params_select = ParamsInputSelect.objects.filter(app_id=pk)
                params_option = {}
                for select in params_select:
                    options = ParamInputOption.objects.filter(select_id=select.pk)
                    params_option[select] = options
                company_name = MyCompany.objects.all()[:1].get()
                current_user = request.user
                try:
                    tasks = Task.objects.filter(user=current_user)
                except Task.DoesNotExist:
                    tasks = None
                context = {
                    'apps': apps,
                    'user': current_user,
                    'tasks': tasks,
                    'company_name': company_name,
                    'app_select': app_select,
                    'params_file': params_file,
                    'params_text': params_text,
                    'params_select': params_select,
                    'params_option': params_option,
                    'taskform': taskform,
                    'error_format_input':'true',
                }
                return render(request, "form_app.html", context)
            else:
                command += " " + request.POST['file_input_option'] + " " + request.FILES['file_input'].name
        if 'file_output_option' in request.POST:
            param_file_output = ParamsInputFile.objects.get(app_id=app_select.pk, type='output')
            list_output = param_file_output.allowed_format.split(',')
            encontrado = False
            for output in list_output:
                if request.FILES['file_output'].name.endswith(str(output)):
                    encontrado = True
            if not encontrado:
                apps = App.objects.all()
                app_select = App.objects.get(pk=pk)
                taskform = TaskForm()
                params_file = ParamsInputFile.objects.filter(app_id=pk)
                params_text = ParamsInputText.objects.filter(app_id=pk)
                params_select = ParamsInputSelect.objects.filter(app_id=pk)
                params_option = {}
                for select in params_select:
                    options = ParamInputOption.objects.filter(select_id=select.pk)
                    params_option[select] = options
                company_name = MyCompany.objects.all()[:1].get()
                current_user = request.user
                try:
                    tasks = Task.objects.filter(user=current_user)
                except Task.DoesNotExist:
                    tasks = None
                context = {
                    'apps': apps,
                    'user': current_user,
                    'tasks': tasks,
                    'company_name': company_name,
                    'app_select': app_select,
                    'params_file': params_file,
                    'params_text': params_text,
                    'params_select': params_select,
                    'params_option': params_option,
                    'taskform': taskform,
                    'error_format_output':'true',
                }
                return render(request, "form_app.html", context)
            else:
                command += " " + request.POST['file_output_option'] + " " + request.FILES['file_output'].name

        tasknew.name = command
        tasknew.taskcode = taskcode + "-" + current_user.email + datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        tasknew.app_id = app_select
        tasknew.user = current_user
        tasknew.save()

        # Conexion al FTP
        ftp_host = 'hpccluster.upo.es'
        ftp_user = 'ftpsuser'
        ftp_password = 'd86aewXiGUfxFy4'
        transport = paramiko.Transport((ftp_host, int(22)))
        transport.connect(username=ftp_user, password=ftp_password)
        ftp = paramiko.sftp_client.SFTPClient.from_transport(transport)

        dir_remote = "/home/ftpsuser/input/pending/"+tasknew.taskcode+"/"
        dir_remote_output = "/home/ftpsuser/output/" + tasknew.taskcode + "/"
        ftp.mkdir(dir_remote)
        ftp.mkdir(dir_remote_output)

        local_file = tasknew.file_input.path
        remote_file = dir_remote + os.path.basename(tasknew.file_input.name)

        ftp.put(local_file, remote_file)

        file = ftp.file(dir_remote+'cmd.txt', "w+")
        file.write(tasknew.name)
        file.flush()

        transport.close()


        apps = App.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        try:
            tasks = Task.objects.filter(user=current_user)
        except Task.DoesNotExist:
            tasks = None
        return render(request, "dashboard.html",
                      {'apps': apps, 'user': current_user, 'tasks': tasks, 'company_name': company_name})

# Descargar Tarea

def download_task_view(request, pk):
    # Obtenemos la tarea que vamos a descargar
    task_select = Task.objects.get(pk=pk)

    ftp_host = 'hpccluster.upo.es'
    ftp_user = 'ftpsuser'
    ftp_password = 'd86aewXiGUfxFy4'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=ftp_host, port=22,
                username=ftp_user, password=ftp_password)
    dir_remote_output = "output/" + task_select.taskcode + "/"
    nombre_zip = task_select.app.name + "-" + task_select.user.email + ".zip"

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python script_tar.py '" + nombre_zip + "' '"+dir_remote_output+"'")
    ssh.close()



    transport = paramiko.Transport((ftp_host, int(22)))
    transport.connect(username=ftp_user, password=ftp_password)
    ftp = paramiko.sftp_client.SFTPClient.from_transport(transport)

    local_dir = settings.MEDIA_ROOT+"/files/output/"+nombre_zip

    ftp.get(nombre_zip,local_dir)
    transport.close()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=ftp_host, port=22,
                username=ftp_user, password=ftp_password)
    nombre_zip = task_select.app.name + "-" + task_select.user.email + ".zip"

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("rm " + nombre_zip + "")
    ssh.close()

    if os.path.exists(local_dir):
        with open(local_dir, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(local_dir)
            return response
    raise Http404

def check_state_task_view(request, pk):
    # Obtenemos la tarea que vamos a descargar
    task_select = Task.objects.get(pk=pk)
    server = 'hpccluster.upo.es'
    username = 'ftpsuser'
    password = 'd86aewXiGUfxFy4'
    # Conexion por SSH

    transport = paramiko.Transport((server, int(22)))
    transport.connect(username=username, password=password)
    ftp = paramiko.sftp_client.SFTPClient.from_transport(transport)
    path_dir ="/home/ftpsuser/input/pending/"+task_select.taskcode
    try:
        ftp.stat(path_dir)
        state = 'PENDING'
        task_select.state = state.lower()
        apps = App.objects.all()
        app_task = App.objects.get(pk=task_select.app.pk)
        compatibility = app_task.app_compatibility.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        context = {
            'apps': apps,
            'user': current_user,
            'task_select': task_select,
            'company_name': company_name,
            'compatibility': compatibility,
            'check_state': state,
        }
        return render(request, "form_task.html", context)
    except IOError, e:
        pass
    transport.close()
    ftp.close()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=server, port=22,
                   username=username, password=password)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python script_select_db.py '"+task_select.taskcode+"'")
    stdin, stdout, stderr = ssh.exec_command('cat /home/ftpsuser/state_job.txt')
    remote_file = stdout.readlines()
    if not remote_file:
        task_select.state = 'in_queue'
        state = 'IN QUEUE'
    else:
        state = str(remote_file[2]).split('+')[0]
        task_select.state = state.lower()
    ssh.close()

    apps = App.objects.all()
    app_task = App.objects.get(pk=task_select.app.pk)
    compatibility = app_task.app_compatibility.all()
    company_name = MyCompany.objects.all()[:1].get()
    current_user = request.user
    context = {
        'apps': apps,
        'user': current_user,
        'task_select': task_select,
        'company_name': company_name,
        'compatibility': compatibility,
        'check_state':state,
    }
    return render(request, "form_task.html", context)


class AppListViewAlt(ListView):
    model = App


class TaskListViewAlt(ListView):
    model = Task


def change_password(request):
    company_name = MyCompany.objects.all()[:1].get()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request, 'change_password.html', {
                'form': form, 'success_password': 'true', 'company_name': company_name})
        else:
            form = PasswordChangeForm(request.user)
            return render(request, 'change_password.html', {
                'form': form, 'error_password':'true','company_name': company_name})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,'company_name': company_name})


def forget_password(request):
    company_name = MyCompany.objects.all()[:1].get()
    form = UserPasswordForm()
    return render(request, 'forgot_password.html', {
                'form': form,'company_name': company_name})

def send_password(request):
    company_name = MyCompany.objects.all()[:1].get()
    userform = UserPasswordForm(request.POST)
    user = User.objects.filter(email=userform.cleaned_data['email'])
    form = UserPasswordForm()
    if not user:
        return render(request, 'forgot_password.html', {
            'form': form, 'company_name': company_name,'error_email':'true'})
    else:
        user = User.objects.get(email=userform.cleaned_data['email'])
        password_new = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_=+)') for i in range(32)])
        user.set_password(password_new)
        user.save()
        asunto = "Change password in GGAFE " + user.email
        mensaje = "The password has been changed, the new password is: " + password_new
        mail = EmailMessage(asunto, mensaje, to=[user.email])
        mail.send()
        return render(request, 'forgot_password.html', {
                'form': form,'company_name': company_name,'password_sent':'true'})

class UserUpdate(UpdateView):
    model = User
    second_model = Profile
    template_name = 'edit_profile.html'
    form_class = EditForm
    second_form_class = ProfileForm
    success_url = reverse_lazy('principal:list-apps-view')

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user = self.model.objects.get(id=pk)
        profile = self.second_model.objects.get(user=user)
        if 'userform' not in context:
            context['userform'] = self.form_class(instance=user)
        if 'userprofileform' not in context:
            context['userprofileform'] = self.second_form_class(instance=profile)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_user = kwargs['pk']
        user = self.model.objects.get(id=id_user)
        profile = self.second_model.objects.get(user=user)
        userform = self.form_class(request.POST, instance=user)
        userprofileform = self.second_form_class(request.POST, instance=profile)
        if userform.is_valid() and userprofileform.is_valid():
            userform.save()
            userprofileform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "edit_profile.html",
                          {'userform': userform, 'userprofileform': userprofileform, 'user': current_user,
                           'company_name': company_name})


class UserAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "user_table_admin.html",
                      {'users': users, 'user': current_user, 'company_name': company_name})


class NewUserAdminListView(LoginRequiredMixin, View):
    model = User
    second_model = Profile
    template_name = 'new_user_table_admin.html'
    form_class = UserForm
    second_form_class = ProfileForm
    success_url = reverse_lazy('principal:list-user-admin-view')

    def get(self, request):
        userform = self.form_class()
        profileform = self.second_form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'userform': userform,
            'profileform': profileform,
            'company_name': company_name,
            'new_user': 'true'
        }
        return render(request, "new_user_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        userform = UserForm(request.POST)
        profileform = ProfileForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(userform.cleaned_data['password'])
            user.save()
            usrprof = profileform.save(commit=False)
            usrprof.user = user
            usrprof.subscribed = '1'
            usrprof.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_user_table_admin.html",
                          {'userform': userform, 'profileform': profileform, 'company_name': company_name,
                           'new_user': 'true'})


class EditUserAdminListView(UpdateView):
    model = User
    second_model = Profile
    template_name = 'new_user_table_admin.html'
    form_class = UserForm
    second_form_class = ProfileForm
    success_url = reverse_lazy('principal:list-user-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditUserAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user = self.model.objects.get(id=pk)
        profile = self.second_model.objects.get(user=user)
        if 'userform' not in context:
            context['userform'] = self.form_class(instance=user)
        if 'profileform' not in context:
            context['profileform'] = self.second_form_class(instance=profile)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_user = kwargs['pk']
        user = self.model.objects.get(id=id_user)
        profile = self.second_model.objects.get(user=user)
        userform = self.form_class(request.POST, instance=user)
        profileform = self.second_form_class(request.POST, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_user_table_admin.html",
                          {'userform': userform, 'profileform': profileform, 'user': current_user,
                           'company_name': company_name, 'id': id_user})


class DeleteUserAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        User.objects.filter(pk=pk).delete()
        users = User.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "user_table_admin.html",
                      {'users': users, 'user': current_user, 'company_name': company_name, 'user_deleted': 'true'})


class AppAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        apps = App.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "app_table_admin.html",
                      {'apps': apps, 'user': current_user, 'company_name': company_name})


class NewAppAdminListView(LoginRequiredMixin, View):
    model = App
    template_name = 'new_app_table_admin.html'
    form_class = AppForm
    success_url = reverse_lazy('principal:list-app-admin-view')

    def get(self, request):
        appform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'appform': appform,
            'company_name': company_name,
            'new_app': 'true'
        }
        return render(request, "new_app_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        appform = AppForm(request.POST, request.FILES)
        if appform.is_valid():
            appform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_app_table_admin.html",
                          {'appform': appform, 'company_name': company_name, 'new_app': 'true'})


class EditAppAdminListView(UpdateView):
    model = App
    template_name = 'new_app_table_admin.html'
    form_class = AppForm
    success_url = reverse_lazy('principal:list-app-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditAppAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        app = self.model.objects.get(id=pk)
        if 'appform' not in context:
            context['appform'] = self.form_class(instance=app)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_app = kwargs['pk']
        app = self.model.objects.get(id=id_app)
        appform = self.form_class(request.POST, request.FILES, instance=app)
        if appform.is_valid():
            appform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_app_table_admin.html",
                          {'appform': appform, 'user': current_user,
                           'company_name': company_name, 'id': id_app})


class DeleteAppAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        App.objects.filter(pk=pk).delete()
        apps = App.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "app_table_admin.html",
                      {'apps': apps, 'user': current_user, 'company_name': company_name, 'user_deleted': 'true'})


class MyCompanyAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "my_company_table_admin.html",
                      {'user': current_user, 'company_name': company_name})


class EditMyCompanyAdminListView(UpdateView):
    model = MyCompany
    template_name = 'edit_mycompany_table_admin.html'
    form_class = MyCompanyForm
    success_url = reverse_lazy('principal:list-mycompany-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditMyCompanyAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        mycompany = self.model.objects.get(id=pk)
        if 'mycompanyform' not in context:
            context['mycompanyform'] = self.form_class(instance=mycompany)
        context['company_name'] = mycompany
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        mycompany = self.model.objects.get(id=pk)
        mycompanyform = self.form_class(request.POST, request.FILES, instance=mycompany)
        if mycompanyform.is_valid():
            mycompanyform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "edit_mycompany_table_admin.html",
                          {'mycompanyform': mycompanyform, 'user': current_user,
                           'company_name': company_name})


# Backend Admin Task

# List Tasks
class TaskAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        tasks = Task.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user

        return render(request, "task_table_admin.html",
                      {'tasks': tasks, 'user': current_user, 'company_name': company_name})


# Create Task
class NewTaskAdminListView(LoginRequiredMixin, View):
    model = Task
    template_name = 'new_task_table_admin.html'
    form_class = TaskAdminForm
    success_url = reverse_lazy('principal:list-task-admin-view')

    def get(self, request):
        taskform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'taskform': taskform,
            'company_name': company_name,
            'new_task': 'true'
        }
        return render(request, "new_task_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        taskform = TaskAdminForm(request.POST, request.FILES)
        if taskform.is_valid():
            taskform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_task_table_admin.html",
                          {'taskform': taskform, 'company_name': company_name, 'new_task': 'true'})


# Edit Task
class EditTaskAdminListView(UpdateView):
    model = Task
    template_name = 'new_task_table_admin.html'
    form_class = TaskAdminForm
    success_url = reverse_lazy('principal:list-task-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditTaskAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        task = self.model.objects.get(id=pk)
        if 'taskform' not in context:
            context['taskform'] = self.form_class(instance=task)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_task = kwargs['pk']
        task = self.model.objects.get(id=id_task)
        taskform = self.form_class(request.POST, request.FILES, instance=task)
        if taskform.is_valid():
            taskform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_task_table_admin.html",
                          {'taskform': taskform, 'user': current_user,
                           'company_name': company_name, 'id': id_task})


# Delete Task
class DeleteTaskAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        Task.objects.filter(pk=pk).delete()
        tasks = Task.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "task_table_admin.html",
                      {'tasks': tasks, 'user': current_user, 'company_name': company_name, 'task_deleted': 'true'})


# Backend Admin ImageSlideShow

# List ImageSlideShow
class ImageSlideShowAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        images = ImageSlideshow.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "image_table_admin.html",
                      {'images': images, 'user': current_user, 'company_name': company_name})


class NewImageSlideShowAdminListView(LoginRequiredMixin, View):
    model = ImageSlideshow
    template_name = 'new_image_table_admin.html'
    form_class = ImageSlideshowForm
    success_url = reverse_lazy('principal:list-image-admin-view')

    def get(self, request):
        imageform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'imageform': imageform,
            'company_name': company_name
        }
        return render(request, "new_image_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        imageform = ImageSlideshowForm(request.POST, request.FILES)
        if imageform.is_valid():
            imageSlide = ImageSlideshow(image=request.FILES['image'])
            imageSlide.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_image_table_admin.html",
                          {'imageform': imageform, 'company_name': company_name})


class DeleteImageSlideShowAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ImageSlideshow.objects.filter(pk=pk).delete()
        images = ImageSlideshow.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "image_table_admin.html",
                      {'images': images, 'user': current_user, 'company_name': company_name,
                       'image_deleted': 'image_deleted'})


# Backend Admin Param Input

# List Param Input
class ParamInputAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        param_file_count = ParamsInputFile.objects.count()
        param_text_count = ParamsInputText.objects.count()
        param_select_count = ParamsInputSelect.objects.count()
        param_option_count = ParamInputOption.objects.count()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'param_file_count': param_file_count,
            'param_text_count': param_text_count,
            'param_select_count': param_select_count,
            'param_option_count': param_option_count,
            'company_name': company_name,
        }
        return render(request, "param_table_admin.html", context)


# List Param File Input
class ParamInputFileAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        params = ParamsInputFile.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_file_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name})


# Create Param Input File
class NewParamInputFileAdminListView(LoginRequiredMixin, View):
    model = ParamsInputFile
    template_name = 'new_param_file_table_admin.html'
    form_class = ParamFileForm
    success_url = reverse_lazy('principal:list-param-file-admin-view')

    def get(self, request):
        paramform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'paramform': paramform,
            'company_name': company_name,
            'new_param': 'true'
        }
        return render(request, "new_param_file_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        paramform = ParamFileForm(request.POST)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_file_table_admin.html",
                          {'paramform': paramform, 'company_name': company_name, 'new_param': 'true'})


# Edit Param Input File
class EditParamInputFileAdminListView(UpdateView):
    model = ParamsInputFile
    template_name = 'new_param_file_table_admin.html'
    form_class = ParamFileForm
    success_url = reverse_lazy('principal:list-param-file-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditParamInputFileAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        param = self.model.objects.get(id=pk)
        if 'paramform' not in context:
            context['paramform'] = self.form_class(instance=param)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_param = kwargs['pk']
        param = self.model.objects.get(id=id_param)
        paramform = self.form_class(request.POST, instance=param)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_file_table_admin.html",
                          {'paramform': paramform, 'user': current_user,
                           'company_name': company_name, 'id': id_param})


# Delete Param Input File
class DeleteParamInputFileAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ParamsInputFile.objects.filter(pk=pk).delete()
        params = ParamsInputFile.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_file_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name, 'param_deleted': 'true'})


# List Param File Text
class ParamInputTextAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        params = ParamsInputText.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_text_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name})


# Create Param Input Text
class NewParamInputTextAdminListView(LoginRequiredMixin, View):
    model = ParamsInputText
    template_name = 'new_param_text_table_admin.html'
    form_class = ParamTextForm
    success_url = reverse_lazy('principal:list-param-text-admin-view')

    def get(self, request):
        paramform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'paramform': paramform,
            'company_name': company_name,
            'new_param': 'true'
        }
        return render(request, "new_param_text_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        paramform = ParamTextForm(request.POST)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_text_table_admin.html",
                          {'paramform': paramform, 'company_name': company_name, 'new_param': 'true'})


# Edit Param Input Text
class EditParamInputTextAdminListView(UpdateView):
    model = ParamsInputText
    template_name = 'new_param_text_table_admin.html'
    form_class = ParamTextForm
    success_url = reverse_lazy('principal:list-param-text-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditParamInputTextAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        param = self.model.objects.get(id=pk)
        if 'paramform' not in context:
            context['paramform'] = self.form_class(instance=param)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_param = kwargs['pk']
        param = self.model.objects.get(id=id_param)
        paramform = self.form_class(request.POST, instance=param)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_text_table_admin.html",
                          {'paramform': paramform, 'user': current_user,
                           'company_name': company_name, 'id': id_param})


# Delete Param Text
class DeleteParamInputTextAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ParamsInputText.objects.filter(pk=pk).delete()
        params = ParamsInputText.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_text_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name, 'param_deleted': 'true'})


# List Param File Option
class ParamInputOptionAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        params = ParamInputOption.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_option_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name})


# Create Param Input Option
class NewParamInputOptionAdminListView(LoginRequiredMixin, View):
    model = ParamInputOption
    template_name = 'new_param_option_table_admin.html'
    form_class = ParamOptionForm
    success_url = reverse_lazy('principal:list-param-option-admin-view')

    def get(self, request):
        paramform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'paramform': paramform,
            'company_name': company_name,
            'new_param': 'true'
        }
        return render(request, "new_param_option_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        paramform = ParamOptionForm(request.POST)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_option_table_admin.html",
                          {'paramform': paramform, 'company_name': company_name, 'new_param': 'true'})


# Edit Param Input Option
class EditParamInputOptionAdminListView(UpdateView):
    model = ParamInputOption
    template_name = 'new_param_option_table_admin.html'
    form_class = ParamOptionForm
    success_url = reverse_lazy('principal:list-param-option-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditParamInputOptionAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        param = self.model.objects.get(id=pk)
        if 'paramform' not in context:
            context['paramform'] = self.form_class(instance=param)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_param = kwargs['pk']
        param = self.model.objects.get(id=id_param)
        paramform = self.form_class(request.POST, instance=param)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_option_table_admin.html",
                          {'paramform': paramform, 'user': current_user,
                           'company_name': company_name, 'id': id_param})


# Delete Param Option
class DeleteParamInputOptionAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ParamInputOption.objects.filter(pk=pk).delete()
        params = ParamInputOption.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_option_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name, 'param_deleted': 'true'})


# List Param File Select
class ParamInputSelectAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        params = ParamsInputSelect.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_select_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name})


# Create Param Input Select
class NewParamInputSelectAdminListView(LoginRequiredMixin, View):
    model = ParamsInputSelect
    template_name = 'new_param_select_table_admin.html'
    form_class = ParamSelectForm
    success_url = reverse_lazy('principal:list-param-select-admin-view')

    def get(self, request):
        paramform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'paramform': paramform,
            'company_name': company_name,
            'new_param': 'true'
        }
        return render(request, "new_param_select_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        paramform = ParamSelectForm(request.POST)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_select_table_admin.html",
                          {'paramform': paramform, 'company_name': company_name, 'new_param': 'true'})


# Edit Param Input Select
class EditParamInputSelectAdminListView(UpdateView):
    model = ParamsInputSelect
    template_name = 'new_param_select_table_admin.html'
    form_class = ParamSelectForm
    success_url = reverse_lazy('principal:list-param-select-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditParamInputSelectAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        param = self.model.objects.get(id=pk)
        if 'paramform' not in context:
            context['paramform'] = self.form_class(instance=param)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_param = kwargs['pk']
        param = self.model.objects.get(id=id_param)
        paramform = self.form_class(request.POST, instance=param)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_select_table_admin.html",
                          {'paramform': paramform, 'user': current_user,
                           'company_name': company_name, 'id': id_param})


# Delete Param Select
class DeleteParamInputSelectAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ParamsInputSelect.objects.filter(pk=pk).delete()
        params = ParamsInputSelect.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_select_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name, 'param_deleted': 'true'})


# Backend Admin Section

# List Sections
class SectionAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        sections = Section.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "section_table_admin.html",
                      {'sections': sections, 'user': current_user, 'company_name': company_name})


# Create Section
class NewSectionAdminListView(LoginRequiredMixin, View):
    model = Section
    template_name = 'new_section_table_admin.html'
    form_class = SectionForm
    success_url = reverse_lazy('principal:list-section-admin-view')

    def get(self, request):
        sectionform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'sectionform': sectionform,
            'company_name': company_name,
            'new_section': 'true'
        }
        return render(request, "new_section_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        sectionform = SectionForm(request.POST, request.FILES)
        if sectionform.is_valid():
            sectionform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_section_table_admin.html",
                          {'sectionform': sectionform, 'company_name': company_name, 'new_section': 'true'})


# Edit Section
class EditSectionAdminListView(UpdateView):
    model = Section
    template_name = 'new_section_table_admin.html'
    form_class = SectionForm
    success_url = reverse_lazy('principal:list-section-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditSectionAdminListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        section = self.model.objects.get(id=pk)
        if 'sectionform' not in context:
            context['sectionform'] = self.form_class(instance=section)
        context['id'] = pk
        context['company_name'] = MyCompany.objects.all()[:1].get()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_section = kwargs['pk']
        section = self.model.objects.get(id=id_section)
        sectionform = self.form_class(request.POST, request.FILES, instance=section)
        if sectionform.is_valid():
            sectionform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_section_table_admin.html",
                          {'sectionform': sectionform, 'user': current_user,
                           'company_name': company_name, 'id': id_section})


# Delete Section
class DeleteSectionAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        Section.objects.filter(pk=pk).delete()
        sections = Section.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "section_table_admin.html",
                      {'sections': sections, 'user': current_user, 'company_name': company_name,
                       'section_deleted': 'true'})
