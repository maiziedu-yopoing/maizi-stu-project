#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/2
@author: yopoing
Admin管理，Admin后台管理配置。
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.text import capfirst
from django.utils.datastructures import OrderedDict
from common.models import *


# 让admin添加model时按照注册的先后顺序添加
def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner


registry = OrderedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)


# 用户管理类
class UserProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


# 章节资源管理类
class LessonResourceInline(admin.TabularInline):
    model = LessonResource


# 章节管理类
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonResourceInline, ]


# 课程资源管理类
class CourseResourceInline(admin.TabularInline):
    model = CourseResource


# 课程管理类
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseResourceInline, ]


# 向admin注册Model
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Ad)
admin.site.register(MyMessage)
admin.site.register(Links)
admin.site.register(Keywords)
admin.site.register(RecommendKeywords)
admin.site.register(EmailVerifyRecord)
admin.site.register(RecommendedReading)
admin.site.register(CareerCourse)
admin.site.register(Stage)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(MyCourse)
admin.site.register(MyFavorite)
admin.site.register(UserLearningLesson)
admin.site.register(UserUnlockStage)
admin.site.register(Class)
admin.site.register(ClassStudents)
admin.site.register(Discuss)
admin.site.register(UserPurchase)
