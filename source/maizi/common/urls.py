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
    url(r'^get_recommend_keywords$', 'get_recommend_keywords', name='get_recommend_keywords'),
)
