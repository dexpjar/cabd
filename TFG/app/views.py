# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import timestamp as timestamp
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, FormView

from app.forms import RegisterForm, ProfileForm, EditForm, LoginForm, TaskForm
from app.models import App, User, Profile, Task, Section, MyCompany, ImageSlideshow, ParamsInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.utils import six


#Funcion que comprueba que los campos del registro son validos y crea el usuario
def create_user_view(request):
    if request.method == 'POST':
        register = RegisterForm(request.POST, prefix='register')
        usrprofile = ProfileForm(request.POST, prefix='profile')
        user = User.objects.get(email=register.cleaned_data['email'])
        if user:
            userform = RegisterForm(request.POST, prefix='register')
            userprofileform = ProfileForm(request.POST, prefix='profile')
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, 'register.html',
                          {'company_name': company_name, 'userform': userform, 'userprofileform': userprofileform, 'email_exist': True})
        else:
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
                asunto = "Account New "+ user.email
                mensaje = "The user with email: "+ user.email+ "is trying to login, you have to active this account through the admin panel"
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
        return render(request, 'register.html', {'company_name': company_name, 'userform': userform, 'userprofileform': userprofileform})

class Login(FormView):
    # Establecemos la plantilla a utilizar
    template_name = 'index.html'
    # Le indicamos que el formulario a utilizar es el formulario de autenticación de Django
    form_class = AuthenticationForm
    form_class.base_fields['username'].widget.attrs['class'] = "form-control"
    form_class.base_fields['password'].widget.attrs['class'] = "form-control"
    form_class.company_name = MyCompany.objects.all()[:1].get()
    form_class.first_slideshow = ImageSlideshow.objects.all()[:1].get()
    form_class.slideshows = ImageSlideshow.objects.all()
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

def contact_view(request):
    company_name = MyCompany.objects.all()[:1].get()
    context = {
        'company_name': company_name,
    }
    return render(request, 'contact.html', context)

@login_required
def detail_app_view(request,pk):
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
def tasks_app_view(request,pk):
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
        return render(request, "dashboard.html", {'apps': apps, 'user': current_user, 'tasks': tasks, 'company_name': company_name})

class AppFormView(LoginRequiredMixin, View):
    def get(self, request, pk):
        apps = App.objects.all()
        app_select = App.objects.get(pk=pk)
        params = ParamsInput.objects.filter(app_id=pk)
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
            'params': params,
        }
        return render(request, "form_app.html", context)

def create_task_view(request,pk):
    if request.method == 'POST':
        app_select = App.objects.get(pk=pk)
        params_ids = ParamsInput.objects.filter(app_id=pk)
        ids = [str(param_id.id) for param_id in params_ids]
        command=  app_select.command
        taskcode = app_select.name
        current_user = request.user
        for param_id in ids:
            valor = request.POST[param_id]
            param = ParamsInput.objects.get(pk=param_id)
            if valor:
                command += " " + param.option + " " + valor
            else:
                command += " " + param.option
            if param.is_file_input:
                file_input = valor
            if param.is_file_output:
                file_output = valor

        new_task = Task.objects.create()
        new_task.name = command
        new_task.taskcode = taskcode
        new_task.app = app_select
        new_task.app_id = app_select
        new_task.user = current_user
        new_task.file_input = file_input
        new_task.file_output = file_output
        new_task.save()
        apps = App.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        try:
            tasks = Task.objects.filter(user=current_user)
        except Task.DoesNotExist:
            tasks = None
        return render(request, "dashboard.html",
                      {'apps': apps, 'user': current_user, 'tasks': tasks, 'company_name': company_name})


class AppListViewAlt(ListView):
    model = App

class TaskListViewAlt(ListView):
    model = Task


def change_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, pk=pk)
    userform = EditForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })
    userprofileform = ProfileForm(initial={
        'institution': profile.institution,
    })

    context = {
        'userform': userform,
        'userprofileform': userprofileform
    }
    return render(request, 'edit_profile.html', context)

class UserUpdate(UpdateView):
    model = User
    second_model = Profile
    template_name = 'edit_profile.html'
    form_class = EditForm
    second_form_class = ProfileForm
    success_url = reverse_lazy('principal:list-apps-view')

    def get_context_data(self, **kwargs):
        context = super(UserUpdate,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        user = self.model.objects.get(id = pk)
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
        userform = self.form_class(request.POST,instance=user)
        userprofileform = self.second_form_class(request.POST, instance=profile)
        if userform.is_valid() and userprofileform.is_valid():
            userform.save()
            userprofileform.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            current_user = request.user
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "edit_profile.html", {'userform': userform, 'userprofileform': userprofileform, 'user': current_user, 'company_name': company_name})