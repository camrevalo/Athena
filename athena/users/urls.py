from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
       
        url(r'^login/$', views.user_login, name='login'),
	url(r'^profile/(?P<user_id>\d*)/$', views.user_profile, name='profile'),
	url(r'^profile/$', views.user_profile, name='profile'),
	url(r'^edit_profile/$', views.edit_user_profile, name='edit_profile'),
        url(r'^$', views.user_login, name='login'),
	)
