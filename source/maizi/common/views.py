#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/21
@author: 彭新
Common模块View业务处理。
"""

from django.shortcuts import render
from common.models import Links, RecommendedReading, UserProfile, Ad, Course, Lesson, RecommendKeywords, CareerCourse
from django.conf import settings
from django.db.models import Sum
from utils import my_pagination
import json
from django.http import HttpResponse
import math


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


def get_course_by_post(request):
    result = {"error": ""}
    pagesize = 10
    course_by = request.POST.get("course_by", "")
    try:
        page = int(request.POST.get("page", 1))
        if page <= 0:
            page = 1
    except:
        page = 1
    if course_by:
        if course_by == "date_publish":
            total_count = Course.objects.filter(is_homeshow=1).count()
            total_pages = math.ceil(total_count / page)
            if page > total_pages:
                page = total_pages
            start, end = get_page_start_and_end(page, pagesize)
            course = Course.objects.filter(is_homeshow=1).order_by("-date_publish", "index")[start:end]
            result["total_pages"] = total_pages
            result["current_page"] = page
            result["data"] = get_return_data(course, course_by)
        elif course_by == "play_times":
            total_count = Lesson.objects.all().values("course").annotate(total_play_count=Sum('play_count')).count()
            total_pages = math.ceil(total_count / page)
            if page > total_pages:
                page = total_pages
            start, end = get_page_start_and_end(page, pagesize)
            course = Lesson.objects.all().values("course__name", "course__student_count", "course__image",
                                                 "course__id").annotate(total_play_count=Sum('play_count')).order_by(
                '-total_play_count')[start:end]
            result["total_pages"] = total_pages
            result["current_page"] = page
            result["data"] = get_return_data(course, course_by)
        elif course_by == "hot":
            total_count = Course.objects.filter(is_homeshow=1).count()
            total_pages = math.ceil(total_count / page)
            if page > total_pages:
                page = total_pages
            start, end = get_page_start_and_end(page, pagesize)
            course = Course.objects.filter(is_homeshow=1).order_by("-favorite_count", "index")[start:end]
            result["total_pages"] = total_pages
            result["current_page"] = page
            result["data"] = get_return_data(course, course_by)
        else:
            result["error"] = "参数错误"
    else:
        result["error"] = "找不到传递的参数"
    print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_page_start_and_end(page, pagesize):
    start = (page - 1) * pagesize
    end = page * pagesize
    return start, end


def get_return_data(course, course_by):
    data = []
    if course_by == "play_times":
        for cc in course:
            data.append((cc.course__name, cc.course__student_count, cc.course__image, cc.course__id))
    else:
        for cc in course:
            data.append((cc.name, cc.student_count, cc.image, cc.id))
    return data


def get_recommend_keywords(request):
    data = []
    keywords = RecommendKeywords.objects.all()
    for i in keywords:
        data.append({'name': i.name})
    return HttpResponse(json.dumps(data), content_type="application/json")


def search_course(request):
    data = dict()
    keyword = request.GET.get("keyword", "")
    if keyword:
        career_course = CareerCourse.objects.filter(name__icontains=keyword).order_by("index")
        course = Course.objects.filter(name__icontains=keyword).order_by("index")
    else:
        career_course = CareerCourse.objects.all().order_by("index")
        course = Course.objects.all().order_by("index")
    data["career_course"] = []
    for i in career_course:
        data["career_course"].append({'name': i.name, 'course_color': i.course_color, 'id': i.id})
    data["course"] = []
    for i in course:
        data["course"].append({'name': i.name, 'id': i.id})
    return HttpResponse(json.dumps(data), content_type="application/json")
