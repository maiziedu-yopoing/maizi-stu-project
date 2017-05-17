#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
common模块的url配置。
"""

from django.conf.urls import url,include
from common import views
from django.conf import settings
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"^uploads/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT,},
    ),
]
