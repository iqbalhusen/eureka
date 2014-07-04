'''
Created on 18-May-2014

@author: iqbal
'''
from django.conf.urls import patterns, url
from eureka import views

urlpatterns = patterns(
                       '',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^submit_manuscript/$', views.submit_manuscript, name='submit_manuscript'),
                       url(r'^category/(?P<category_name_url>\w+)/$', views.category, name = 'category'),
                       url(r'^category/(?P<category_name_url>\w+)/popular/$', views.popular, name = 'popular'),
                       url(r'^category/(?P<category_name_url>\w+)/current_issue/$', views.current_issue, name = 'current_issue'),
                       url(r'^category/(?P<category_name_url>\w+)/archive/$', views.archive, name = 'archive'),
                       url(r'^category/(?P<category_name_url>\w+)/archive/(?P<volume_num>\d+)/(?P<issue_num>\d+)/$', views.archive_volume_issue, name = 'archive_volume_issue'),
                       url(r'^category/(?P<category_name_url>\w+)/article/(?P<article_num>\d+)/$', views.article, name = 'article'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^like_category/$', views.like_category, name='like_category'),
                       url(r'^view_article/$', views.view_article, name='view_article'),
                       url(r'^view_category/$', views.view_category, name='view_category'),
                       url(r'^like_article/$', views.like_article, name='like_article'),
                       url(r'^unlike_article/$', views.unlike_article, name='unlike_article'),
                       url(r'^unlike_category/$', views.unlike_category, name='unlike_category'),
                       url(r'^search_article/$', views.search_article, name='search_article'),
                       url(r'^(?P<username>\w+)/$', views.pub_profile, name = 'pub_profile'),
                       )