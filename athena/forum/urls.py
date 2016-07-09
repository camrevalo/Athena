from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
	url(r'^(?P<question_id>\d+)/answer/$', views.answer, name='answer'),
	url(r'^answer/$', views.answer, name='answer'),
	url(r'^add_question/$', views.add_question, name='add_question'),
	url(r'^(?P<question_id>\d+)/upvote/$', views.upvote, name='upvote'),
	url(r'^upvote/$', views.upvote, name='upvote'),
	url(r'^(?P<question_id>\d+)/downvote/$', views.downvote, name='downvote'),
	url(r'^downvote/$', views.downvote, name='downvote'),
        url(r'^filter_index/$', views.filter_index, name='filter_index'),
)
