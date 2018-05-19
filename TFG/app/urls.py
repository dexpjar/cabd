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
    DeleteTaskAdminListView, NewTaskAdminListView, NewParamInputAdminListView, DeleteParamInputAdminListView, \
    EditParamInputAdminListView

urlpatterns = [
    url(r'^create_user/$',create_user_view, name = 'create-user-view'),
    url(r'^detail/(?P<pk>\d+)$', detail_app_view, name='detail-apps-view'),
    url(r'^tasks/(?P<pk>\d+)$', tasks_app_view, name='tasks-apps-view'),
    url(r'^app/form/(?P<pk>\d+)$', login_required(AppFormView.as_view()), name='form-apps-view'),
    url(r'^dashboard/$', login_required(AppListView.as_view()), name='list-apps-view'),
    url(r'^user/edit/(?P<pk>\d+)$', login_required(UserUpdate.as_view()), name='edit-user-view'),
    url(r'^user/password/(?P<pk>\d+)$', change_password, name='change-password'),
    url(r'^contact/$', contact_view, name='contact-view'),
    url(r'^create_task/(?P<pk>\d+)$',login_required(create_task_view), name = 'create-task-view'),
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
    url(r'^new_param_admin_view/$', login_required(NewParamInputAdminListView.as_view()), name='new-param-admin-view'),
    url(r'^delete_param_admin_view/(?P<pk>\d+)$', login_required(DeleteParamInputAdminListView.as_view()), name='delete-param-admin-view'),
    url(r'^edit_param_admin_view/(?P<pk>\d+)$', login_required(EditParamInputAdminListView.as_view()), name='edit-param-admin-view'),

    # Admin Section
    url(r'^section_admin_view/$', login_required(SectionAdminListView.as_view()), name='list-section-admin-view'),
    url(r'^new_section_admin_view/$', login_required(NewSectionAdminListView.as_view()), name='new-section-admin-view'),
    url(r'^delete_section_admin_view/(?P<pk>\d+)$', login_required(DeleteSectionAdminListView.as_view()), name='delete-section-admin-view'),
    url(r'^edit_section_admin_view/(?P<pk>\d+)$', login_required(EditSectionAdminListView.as_view()), name='edit-section-admin-view'),
]