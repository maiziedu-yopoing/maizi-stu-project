#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/21
@author: 彭新
Common模块View业务处理。
"""

from django.shortcuts import render
from common.models import Links, RecommendedReading, UserProfile, Ad, Course, Lesson, RecommendKeywords
from django.conf import settings
from django.db.models import Sum
from utils import my_pagination
import json
from django.http import HttpResponse


# 首页
def index(request):
    media_url = settings.MEDIA_URL
    ads = Ad.objects.order_by("index")
    teachers = UserProfile.objects.filter(groups__name='老师')
    links = Links.objects.all()

    course_lastest = Course.objects.filter(is_homeshow=1).order_by("-date_publish", "index")
    course_lastest, paginator_lastest = my_pagination(request, course_lastest, "pgl")

    course_most_play = Lesson.objects.all().values("course__name", "course__student_count", "course__image",
                                                   "course__id").annotate(total_play_count=Sum('play_count')).order_by(
        '-total_play_count')
    course_most_play, paginator_most_play = my_pagination(request, course_most_play, "pgm")

    course_hot = Course.objects.filter(is_homeshow=1).order_by("-favorite_count", "index")
    course_hot, paginator_hot = my_pagination(request, course_hot, "pgh")

    recommend_av = RecommendedReading.objects.filter(reading_type=RecommendedReading.ACTIVITY)
    recommend_nw = RecommendedReading.objects.filter(reading_type=RecommendedReading.NEWS)
    recommend_dc = RecommendedReading.objects.filter(reading_type=RecommendedReading.DISCUSS)
    return render(request, "common/index.html", locals())


def get_recommend_keywords(request):
    data = []
    keywords = RecommendKeywords.objects.all()
    for i in keywords:
        data.append({'name': i.name})
    return HttpResponse(json.dumps(data), content_type="application/json")
