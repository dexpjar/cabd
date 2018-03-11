from django.conf.urls import url

from app.views import detail_app_view, AppListView, create_user_view, \
    create_user_view, change_password, UserUpdate, contact_view

urlpatterns = [
    url(r'^create_user/$',create_user_view, name = 'create-user-view'),
    url(r'^detail/(?P<pk>\d+)$', detail_app_view, name='detail-apps-view'),
    url(r'^dashboard/$', AppListView.as_view(), name='list-apps-view'),
    url(r'^user/edit/(?P<pk>\d+)$', UserUpdate.as_view(), name='edit-user-view'),
    url(r'^user/password/(?P<pk>\d+)$', change_password, name='change-password'),
    url(r'^contact/$', contact_view, name='contact-view'),
]

# create_user_view,