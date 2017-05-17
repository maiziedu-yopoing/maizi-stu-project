#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017/05/16
@author: victor chi
Common模块View业务处理。
"""

from django.shortcuts import render
import logging
from .models import *

# 首页
def index(request):
    try:
        # 获取数据库中所有的友情链接的内容
        link_list = Links.objects.all()
        AV_list = RecommendedReading.objects.filter(reading_type='AV')[:5]
        NW_list = RecommendedReading.objects.filter(reading_type='NW')[:5]
        DC_list = RecommendedReading.objects.filter(reading_type='DC')[:5]
        ad_list = Ad.objects.all()
        # teacher_lisht =
    except Exception as e:
        logging.error(e)
    return render(request, "common/index.html", locals())
