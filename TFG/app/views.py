# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import timestamp as timestamp
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Q
from django import forms
from django.forms.utils import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, FormView

from app.forms import RegisterForm, ProfileForm, EditForm, LoginForm, TaskForm, ImageSlideshowForm, UserForm, AppForm, \
    MyCompanyForm, SectionForm, TaskAdminForm, ParamForm
from app.models import App, User, Profile, Task, Section, MyCompany, ImageSlideshow, ParamsInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.utils import six


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
        user = self.model.objects.get(username= username)
        if not user.is_superuser:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                u'This user is not superuser'
            ])
            return super(AdminLogin, self).form_invalid(form)
        else:
            login(self.request, form.get_user())
            return super(AdminLogin, self).form_valid(form)


def contact_view(request):
    company_name = MyCompany.objects.all()[:1].get()
    context = {
        'company_name': company_name,
    }
    return render(request, 'contact.html', context)


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
    param_count = ParamsInput.objects.count()
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


class create_task_view(CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        file = self.cleaned_data.get('file_input', None)
        form.save()
        return super(self).form_valid(form)

    def create_task_view(request, pk):
        if request.method == 'POST':
            app_select = App.objects.get(pk=pk)
            params_ids = ParamsInput.objects.filter(app_id=pk)
            ids = [str(param_id.id) for param_id in params_ids]
            command = app_select.command
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
            'new_user':'true'
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
                          {'userform': userform, 'profileform': profileform, 'company_name': company_name,'new_user':'true'})


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
                      {'users': users, 'user': current_user, 'company_name': company_name,'user_deleted':'true'})

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
            'new_app':'true'
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
                          {'appform': appform, 'company_name': company_name,'new_app':'true'})


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
                      {'apps': apps, 'user': current_user, 'company_name': company_name,'user_deleted':'true'})

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
            'new_task':'true'
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
                          {'taskform': taskform, 'company_name': company_name,'new_task':'true'})

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
                      {'tasks': tasks, 'user': current_user, 'company_name': company_name,'task_deleted':'true'})


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
        imageform = ImageSlideshowForm(request.POST,request.FILES)
        if imageform.is_valid():
            imageSlide = ImageSlideshow(image = request.FILES['image'])
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
                      {'images': images, 'user': current_user, 'company_name': company_name,'image_deleted': 'image_deleted'})


# Backend Admin Param Input

# List Param Input
class ParamInputAdminListView(LoginRequiredMixin, View):
    def get(self, request):
        params = ParamsInput.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name})

# Create Param Input
class NewParamInputAdminListView(LoginRequiredMixin, View):
    model = ParamsInput
    template_name = 'new_param_table_admin.html'
    form_class = ParamForm
    success_url = reverse_lazy('principal:list-param-admin-view')


    def get(self, request):
        paramform = self.form_class()
        company_name = MyCompany.objects.all()[:1].get()
        context = {
            'paramform': paramform,
            'company_name': company_name,
            'new_param':'true'
        }
        return render(request, "new_param_table_admin.html", context)

    def post(self, request, *args, **kwargs):
        paramform = ParamForm(request.POST)
        if paramform.is_valid():
            paramform.save()
            return HttpResponseRedirect(self.success_url)
        else:
            company_name = MyCompany.objects.all()[:1].get()
            return render(request, "new_param_table_admin.html",
                          {'paramform': paramform, 'company_name': company_name,'new_param':'true'})

# Edit Param Input
class EditParamInputAdminListView(UpdateView):
    model = ParamsInput
    template_name = 'new_param_table_admin.html'
    form_class = ParamForm
    success_url = reverse_lazy('principal:list-param-admin-view')

    def get_context_data(self, **kwargs):
        context = super(EditParamInputAdminListView, self).get_context_data(**kwargs)
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
            return render(request, "new_param_table_admin.html",
                          {'paramform': paramform, 'user': current_user,
                           'company_name': company_name, 'id': id_param})

# Delete Param Input
class DeleteParamInputAdminListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ParamsInput.objects.filter(pk=pk).delete()
        params = ParamsInput.objects.all()
        company_name = MyCompany.objects.all()[:1].get()
        current_user = request.user
        return render(request, "param_table_admin.html",
                      {'params': params, 'user': current_user, 'company_name': company_name,'param_deleted':'true'})

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
            'new_section':'true'
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
                          {'sectionform': sectionform, 'company_name': company_name,'new_section':'true'})

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
                      {'sections': sections, 'user': current_user, 'company_name': company_name,'section_deleted':'true'})