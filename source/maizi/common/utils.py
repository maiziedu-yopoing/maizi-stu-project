#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/21
@author: peng
功能描述
"""
from django.core.paginator import Paginator


def my_pagination(request, queryset, page_name, display_amount=10, after_range_num=5, bevor_range_num=4):
    paginator = Paginator(queryset, display_amount)
    try:
        page = int(request.GET.get(page_name))
    except:
        page = 1
    try:
        objects = paginator.page(page)
    except:
        objects = paginator.page(1)
    # 根据参数配置导航显示范围
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + bevor_range_num]
    else:
        page_range = paginator.page_range[0:page + bevor_range_num]
    return objects, page_range
