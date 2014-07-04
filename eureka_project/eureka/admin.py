'''
Created on 18-May-2014

@author: iqbal
'''

from django.contrib import admin
from eureka.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'likes')

class LikeArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')

class LikeCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'isOutsider', 'profession')

admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(LikeCategory, LikeCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(LikeArticle, LikeArticleAdmin)