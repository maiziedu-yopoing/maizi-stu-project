#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
common模块的url配置。
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'common.views',
    url(r'^$', 'index', name='index'),
    url(r'^get_recommend_keywords/$', 'get_recommend_keywords', name='get_recommend_keywords'),
    url(r'^get_course_by_post/$', 'get_course_by_post', name='get_course_by_post'),
    url(r'^search_course/$', 'search_course', name='search_course'),
    url(r'^teacher_course/(?P<teacher_id>\d+)$', 'teacher_course', name='teacher_course'),
)
