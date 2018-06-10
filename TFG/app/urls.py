from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views import detail_app_view, AppListView, create_user_view, \
    create_user_view, change_password, UserUpdate, contact_view, AppFormView, create_task_view, tasks_app_view, \
    admin_view, UserAdminListView, AppAdminListView, MyCompanyAdminListView, TaskAdminListView, \
    ImageSlideShowAdminListView, ParamInputAdminListView, SectionAdminListView, NewImageSlideShowAdminListView, \
    DeleteImageSlideShowAdminListView, DeleteUserAdminListView, NewUserAdminListView, EditUserAdminListView, \
    NewAppAdminListView, DeleteAppAdminListView, EditAppAdminListView, EditMyCompanyAdminListView, \
    NewSectionAdminListView, DeleteSectionAdminListView, EditSectionAdminListView, EditTaskAdminListView, \
    DeleteTaskAdminListView, NewTaskAdminListView, \
    ParamInputFileAdminListView, NewParamInputFileAdminListView, EditParamInputFileAdminListView, \
    DeleteParamInputFileAdminListView, ParamInputTextAdminListView, NewParamInputTextAdminListView, \
    DeleteParamInputTextAdminListView, EditParamInputTextAdminListView, ParamInputOptionAdminListView, \
    NewParamInputOptionAdminListView, DeleteParamInputOptionAdminListView, EditParamInputOptionAdminListView, \
    ParamInputSelectAdminListView, NewParamInputSelectAdminListView, DeleteParamInputSelectAdminListView, \
    EditParamInputSelectAdminListView, TaskDetailView, SendAppCompatibilityView, getting_started_view, citations_view, \
    forget_password, send_password, download_task_view, check_state_task_view

urlpatterns = [
    #Registro
    url(r'^create_user/$',create_user_view, name = 'create-user-view'),

    #Ventana detalles aplicacion
    url(r'^detail/(?P<pk>\d+)$', detail_app_view, name='detail-apps-view'),

    #Ventana tabla con las tareas de la aplicacion
    url(r'^tasks/(?P<pk>\d+)$', tasks_app_view, name='tasks-apps-view'),

    #Formulario creacion tarea
    url(r'^app/form/(?P<pk>\d+)$', login_required(AppFormView.as_view()), name='form-apps-view'),

    #Vista detalles de tarea individual
    url(r'^task/detail/(?P<pk>\d+)$', login_required(TaskDetailView.as_view()), name='task-detail-view'),

    #Enviar parametros a aplicacion compatible
    url(r'^send_app_compatibility/(?P<pk>\d+)$', login_required(SendAppCompatibilityView.as_view()), name='send-app-compatibility-view'),

    #Menu principal del dashboard
    url(r'^dashboard/$', login_required(AppListView.as_view()), name='list-apps-view'),

    #Editar usuario
    url(r'^user/edit/(?P<pk>\d+)$', login_required(UserUpdate.as_view()), name='edit-user-view'),

    #Cambiar password
    url(r'^password/$', change_password, name='change_password'),

    #Olvido password
    url(r'^forget_password/$', forget_password, name='forget-password-view'),
    url(r'^send_password/$', send_password, name='send-password-view'),

    #Menu Index
    url(r'^contact/$', contact_view, name='contact-view'),
    url(r'^getting_started/$', getting_started_view, name='getting-started-view'),
    url(r'^citations/$', citations_view, name='citations-view'),

    # Crear Tarea
    url(r'^create_task/(?P<pk>\d+)$',login_required(create_task_view), name = 'create-task-view'),

    # Descargar Tarea
    url(r'^download_task/(?P<pk>\d+)$',login_required(download_task_view), name = 'download-task-view'),

    # Ver Estado Tarea
    url(r'^check_state_task/(?P<pk>\d+)$',login_required(check_state_task_view), name = 'check-state-task-view'),

    # Dashboard admin
    url(r'^admin_view/$', login_required(admin_view), name='admin-view'),


    # Admin User
    url(r'^user_admin_view/$', login_required(UserAdminListView.as_view()), name='list-user-admin-view'),
    url(r'^new_user_admin_view/$', login_required(NewUserAdminListView.as_view()), name='new-user-admin-view'),
    url(r'^delete_user_admin_view/(?P<pk>\d+)$', login_required(DeleteUserAdminListView.as_view()), name='delete-user-admin-view'),
    url(r'^edit_user_admin_view/(?P<pk>\d+)$', login_required(EditUserAdminListView.as_view()), name='edit-user-admin-view'),

    # Admin App
    url(r'^app_admin_view/$', login_required(AppAdminListView.as_view()), name='list-app-admin-view'),
    url(r'^new_app_admin_view/$', login_required(NewAppAdminListView.as_view()), name='new-app-admin-view'),
    url(r'^delete_app_admin_view/(?P<pk>\d+)$', login_required(DeleteAppAdminListView.as_view()), name='delete-app-admin-view'),
    url(r'^edit_app_admin_view/(?P<pk>\d+)$', login_required(EditAppAdminListView.as_view()), name='edit-app-admin-view'),

    # Admin MyCompany
    url(r'^mycompany_admin_view/$', login_required(MyCompanyAdminListView.as_view()), name='list-mycompany-admin-view'),
    url(r'^edit_mycompany_admin_view/(?P<pk>\d+)$', login_required(EditMyCompanyAdminListView.as_view()), name='edit-mycompany-admin-view'),

    # Admin Task
    url(r'^task_admin_view/$', login_required(TaskAdminListView.as_view()), name='list-task-admin-view'),
    url(r'^new_task_admin_view/$', login_required(NewTaskAdminListView.as_view()), name='new-task-admin-view'),
    url(r'^delete_task_admin_view/(?P<pk>\d+)$', login_required(DeleteTaskAdminListView.as_view()), name='delete-task-admin-view'),
    url(r'^edit_task_admin_view/(?P<pk>\d+)$', login_required(EditTaskAdminListView.as_view()), name='edit-task-admin-view'),

    # Admin ImageSlideShow
    url(r'^image_admin_view/$', login_required(ImageSlideShowAdminListView.as_view()), name='list-image-admin-view'),
    url(r'^new_image_admin_view/$', login_required(NewImageSlideShowAdminListView.as_view()), name='new-image-admin-view'),
    url(r'^delete_image_admin_view/(?P<pk>\d+)$', login_required(DeleteImageSlideShowAdminListView.as_view()), name='delete-image-admin-view'),

    # Admin Param Input
    url(r'^param_admin_view/$', login_required(ParamInputAdminListView.as_view()), name='list-param-admin-view'),
    url(r'^param_file_admin_view/$', login_required(ParamInputFileAdminListView.as_view()), name='list-param-file-admin-view'),
    url(r'^new_param_file_admin_view/$', login_required(NewParamInputFileAdminListView.as_view()), name='new-param-file-admin-view'),
    url(r'^delete_param_file_admin_view/(?P<pk>\d+)$', login_required(DeleteParamInputFileAdminListView.as_view()), name='delete-param-file-admin-view'),
    url(r'^edit_param_file_admin_view/(?P<pk>\d+)$', login_required(EditParamInputFileAdminListView.as_view()), name='edit-param-file-admin-view'),

    url(r'^param_text_admin_view/$', login_required(ParamInputTextAdminListView.as_view()), name='list-param-text-admin-view'),
    url(r'^new_param_text_admin_view/$', login_required(NewParamInputTextAdminListView.as_view()), name='new-param-text-admin-view'),
    url(r'^delete_param_text_admin_view/(?P<pk>\d+)$', login_required(DeleteParamInputTextAdminListView.as_view()), name='delete-param-text-admin-view'),
    url(r'^edit_param_text_admin_view/(?P<pk>\d+)$', login_required(EditParamInputTextAdminListView.as_view()), name='edit-param-text-admin-view'),

    url(r'^param_option_admin_view/$', login_required(ParamInputOptionAdminListView.as_view()), name='list-param-option-admin-view'),
    url(r'^new_param_option_admin_view/$', login_required(NewParamInputOptionAdminListView.as_view()), name='new-param-option-admin-view'),
    url(r'^delete_param_option_admin_view/(?P<pk>\d+)$', login_required(DeleteParamInputOptionAdminListView.as_view()), name='delete-param-option-admin-view'),
    url(r'^edit_param_option_admin_view/(?P<pk>\d+)$', login_required(EditParamInputOptionAdminListView.as_view()), name='edit-param-option-admin-view'),

    url(r'^param_select_admin_view/$', login_required(ParamInputSelectAdminListView.as_view()), name='list-param-select-admin-view'),
    url(r'^new_param_select_admin_view/$', login_required(NewParamInputSelectAdminListView.as_view()), name='new-param-select-admin-view'),
    url(r'^delete_param_select_admin_view/(?P<pk>\d+)$', login_required(DeleteParamInputSelectAdminListView.as_view()), name='delete-param-select-admin-view'),
    url(r'^edit_param_select_admin_view/(?P<pk>\d+)$', login_required(EditParamInputSelectAdminListView.as_view()), name='edit-param-select-admin-view'),

    # Admin Section
    url(r'^section_admin_view/$', login_required(SectionAdminListView.as_view()), name='list-section-admin-view'),
    url(r'^new_section_admin_view/$', login_required(NewSectionAdminListView.as_view()), name='new-section-admin-view'),
    url(r'^delete_section_admin_view/(?P<pk>\d+)$', login_required(DeleteSectionAdminListView.as_view()), name='delete-section-admin-view'),
    url(r'^edit_section_admin_view/(?P<pk>\d+)$', login_required(EditSectionAdminListView.as_view()), name='edit-section-admin-view'),
]