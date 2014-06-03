'''
Created on 18-May-2014

@author: iqbal
'''

from django.contrib import admin
from eureka.models import *

admin.site.register(Category)
#admin.site.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)