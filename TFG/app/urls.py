from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from app.views import detail_app_view, AppListView, create_user_view, \
    create_user_view, change_password, UserUpdate, contact_view, AppFormView, create_task_view, tasks_app_view

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
]

# create_user_view,