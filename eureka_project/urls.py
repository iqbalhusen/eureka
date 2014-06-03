'''
Created on 18-May-2014

@author: iqbal
'''

from django.conf.urls import patterns, include, url
from django.conf import settings #This is for serving user uploaded file
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eureka_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^eureka/', include('eureka.urls')),
    #url(r'^media/eureka/', include('eureka.urls'))
    )

#This is for serving user uploaded file
if settings.DEBUG:
        urlpatterns += patterns(
                                    'django.views.static',
                                    (
                                        r'media/eureka/(?P<path>.*)',
                                        'serve',
                                        {'document_root': settings.MEDIA_ROOT}
                                    ),
                                )