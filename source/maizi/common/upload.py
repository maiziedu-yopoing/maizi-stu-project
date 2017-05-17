# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt

# @csrf_exempt
# def upload_image(request,dir_name)
#     pass
