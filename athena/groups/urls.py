from django.conf.urls import patterns, url
from groups import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<group_id>\d+)/$', views.detail, name='detail'),
    url(r'^new/$', views.new, name='new'),
    url(r'^add_group/$', views.add_group, name='add_group'),
    # url(r'^edit/$', views.edit, name='edit'),
    # url(r'^delete/$', views.delete, name='delete'),
)
