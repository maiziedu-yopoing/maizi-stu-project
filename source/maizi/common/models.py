#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015/10/27
@author: yopoing
Model管理，包含各个模块所需要的数据模型，由项目组长统一管理。
'''

from datetime import datetime
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, \
    AbstractBaseUser, PermissionsMixin


class Ad(models.Model):
    '''
    首页广告
    '''

    title = models.CharField(u'广告标题', max_length=50)
    description = models.CharField(u'广告描述', max_length=200)
    # 日期存放路径ad/年/月
    image_url = models.ImageField(u'图片路径', upload_to='ad/%Y/%m')
    callback_url = models.URLField(u'回调url', null=True, blank=True)
    index = models.IntegerField(u'排列顺序(从小到大)', default=999)

    class Meta:
        verbose_name = u'网站广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'ad'

    def __unicode__(self):
        return self.title


class MyMessage(models.Model):
    '''
    我的消息
    '''

    action_types = (
        ('1', u'系统消息'),
        ('2', u'课程讨论回复'),
        ('3', u'论坛讨论回复'),
    )

    # 发送方,为0表示系统用户
    userA = models.IntegerField(u'用户A')
    # 接收方,为0就给所有用户发送消息
    userB = models.IntegerField(u'用户B')
    action_type = models.CharField(u'类型', choices=action_types, max_length=1)
    action_id = models.IntegerField(u'动作id', blank=True, null=True)
    action_content = models.TextField(u'消息内容', blank=True, null=True)
    date_action = models.DateTimeField(u'添加日期', auto_now_add=True)
    is_new = models.BooleanField(u'是否为最新', default=True)

    class Meta:
        verbose_name = u'我的消息'
        verbose_name_plural = verbose_name
        db_table = 'my_message'

    def __unicode__(self):
        return str(self.id)


class Links(models.Model):
    '''
    友情链接
    '''

    title = models.CharField(u'标题', max_length=50)
    description = models.CharField(u'友情链接描述', max_length=200)
    image_url = models.ImageField(u'图片路径', upload_to='links/%Y/%m',
                                  null=True, blank=True)
    callback_url = models.URLField(u'回调url')
    is_pic = models.BooleanField(u'是否为图片', default=False)

    class Meta:
        verbose_name = u'友情链接'
        verbose_name_plural = verbose_name
        db_table = 'links'

    def __unicode__(self):
        return self.title


class Keywords(models.Model):
    '''
    关键词
    '''

    name = models.CharField(u'关键词', max_length=50)

    class Meta:
        verbose_name = u'关键词'
        verbose_name_plural = verbose_name
        db_table = 'keywords'

    def __unicode__(self):
        return self.name


class RecommendKeywords(models.Model):
    '''
    推荐搜索关键词
    '''

    name = models.CharField(u'推荐搜索关键词', max_length=50)

    class Meta:
        verbose_name = u'推荐搜索关键词'
        verbose_name_plural = verbose_name
        db_table = 'recommend_keywords'

    def __unicode__(self):
        return self.name


class EmailVerifyRecord(models.Model):
    '''
    邮箱验证记录
    '''

    code = models.CharField(u'验证码', max_length=10)
    email = models.CharField(u'邮箱', max_length=50)
    type = models.SmallIntegerField(u'验证码类型', default=0,
                                    choices=((0, u'注册'), (1, u'忘记密码'),))
    ip = models.CharField(u'请求来源IP', max_length=20)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'邮箱验证记录'
        verbose_name_plural = verbose_name
        db_table = 'email_verify_record'

    def __unicode__(self):
        return self.code


class RecommendedReading(models.Model):
    '''
    首页推荐文章
    '''

    ACTIVITY = 'AV'
    NEWS = 'NW'
    DISCUSS = 'DC'

    READING_TYPES = (
        (ACTIVITY, '官方活动'),
        (NEWS, '开发者资讯'),
        (DISCUSS, '技术交流'),
    )

    reading_type = models.CharField(u'文章类型', max_length=2,
                                    choices=READING_TYPES, default=ACTIVITY)
    title = models.CharField(u'文章标题', max_length=200)
    url = models.URLField(u'文章链接', max_length=200)

    class Meta:
        verbose_name = u'首页推荐文章'
        verbose_name_plural = verbose_name
        db_table = 'recommended_reading'

    def __unicode__(self):
        return self.title


class CareerCourse(models.Model):
    '''
    职业课程
    '''

    name = models.CharField(u'职业课程名称', max_length=50)
    short_name = models.CharField(u'职业课程英文名称简写', max_length=10, unique=True)
    image = models.ImageField(u'课程小图标', upload_to='course/%Y/%m')
    description = models.TextField(u'文字介绍')
    student_count = models.IntegerField(u'学习人数', default=0)
    market_page_url = models.URLField(u'营销页面地址', blank=True, null=True)
    course_color = models.CharField(u'课程配色', max_length=50, default="#50cd8e")
    discount = models.DecimalField(u'折扣', default=1, max_digits=3, decimal_places=2)
    click_count = models.IntegerField(u'点击次数', default=0)
    index = models.IntegerField(u'职业课程顺序(从小到大)', default=999)
    search_keywords = models.ManyToManyField(Keywords, verbose_name=u'搜索关键词')
    seo_title = models.CharField(u'SEO标题', max_length=200, null=True, blank=True)
    seo_keyword = models.CharField(u'SEO关键词', max_length=200, null=True, blank=True)
    seo_description = models.TextField(u'SEO描述', null=True, blank=True)

    class Meta:
        verbose_name = u'职业课程'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        db_table = 'career_course'

    def __unicode__(self):
        return self.name


class Stage(models.Model):
    '''
    阶段
    '''

    name = models.CharField(u'阶段名称', max_length=50)
    description = models.TextField(u'阶段描述')
    price = models.IntegerField(u'阶段价格')
    index = models.IntegerField(u'阶段顺序(从小到大)', default=999)
    is_try = models.BooleanField(u'是否是试学阶段', default=False)
    career_course = models.ForeignKey(CareerCourse, verbose_name=u'职业课程')

    class Meta:
        verbose_name = '课程阶段'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'stage'

    def __unicode__(self):
        return self.name


class Course(models.Model):
    '''
    课程
    '''

    name = models.CharField(u'课程名称', max_length=50)
    image = models.ImageField(u'课程封面', upload_to='course/%Y/%m')
    image2 = models.ImageField(u'课程小图', upload_to='course/%Y/%m', null=True)
    description = models.TextField(u'课程描述')
    is_active = models.BooleanField(u'有效性', default=True)
    date_publish = models.DateTimeField(u'发布时间', auto_now_add=True)
    need_days = models.IntegerField(u'无基础学生完成天数', default=7)
    need_days_base = models.IntegerField(u'有基础学生完成天数', default=5)
    student_count = models.IntegerField(u'学习人数', default=0)
    favorite_count = models.IntegerField(u'收藏次数', default=0)
    click_count = models.IntegerField(u'点击次数', default=0)
    is_novice = models.BooleanField(u'是否是新手课程', default=False)
    is_click = models.BooleanField(u'是否点击能进入课程', default=False)
    index = models.IntegerField(u'课程顺序(从小到大)', default=999)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'老师')
    stages = models.ForeignKey(Stage, blank=True, null=True, verbose_name=u'阶段')
    search_keywords = models.ManyToManyField(Keywords, verbose_name=u'小课程搜索关键词')
    is_homeshow = models.BooleanField(u'是否在首页显示', default=False)
    is_required = models.BooleanField(u'是否必修', default=True)
    course_color = models.CharField(u'课程配色', max_length=50, default="#429FDA")

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        db_table = 'course'

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    '''
    视频章节
    '''

    name = models.CharField(u'章节名称', max_length=50)
    video_url = models.CharField(u'视频资源URL', max_length=200)
    video_length = models.IntegerField(u'视频长度（秒）')
    play_count = models.IntegerField(u'播放次数', default=0)
    share_count = models.IntegerField(u'分享次数', default=0)
    index = models.IntegerField(u'章节顺序(从小到大)', default=999)
    is_popup = models.BooleanField(u'是否弹出提示框（支付、登录）', default=False)
    course = models.ForeignKey(Course, verbose_name=u'课程')
    seo_title = models.CharField(u'SEO标题', max_length=200, null=True, blank=True)
    seo_keyword = models.CharField(u'SEO关键词', max_length=200, null=True, blank=True)
    seo_description = models.TextField(u'SEO描述', null=True, blank=True)

    class Meta:
        verbose_name = u'视频章节'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'lesson'

    def __unicode__(self):
        return self.name


class LessonResource(models.Model):
    '''
    章节资源
    '''

    name = models.CharField(u'章节资源名称', max_length=50)
    download_url = models.FileField(u'下载地址', upload_to='lesson/%Y/%m')
    download_count = models.IntegerField(u'下载次数', default=0)
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')

    class Meta:
        verbose_name = u'章节资源'
        verbose_name_plural = verbose_name
        db_table = 'lesson_resource'

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    '''
    课程资源
    '''

    name = models.CharField(u'课程资源名称', max_length=50)
    download_url = models.FileField(u'下载地址', upload_to='course/%Y/%m')
    download_count = models.IntegerField(u'下载次数', default=0)
    course = models.ForeignKey(Course, verbose_name=u'课程')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
        db_table = 'course_resource'

    def __unicode__(self):
        return self.name


class UserProfileManager(BaseUserManager):
    '''
    自定义用户管理器
    '''

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        '''
        根据用户名和密码创建一个用户
        '''
        now = datetime.now()
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''
    继承AbstractUser，扩展用户信息
    '''

    username = models.CharField(u'昵称', max_length=30, unique=True)
    first_name = models.CharField(u'名字', max_length=30, blank=True)
    last_name = models.CharField(u'姓氏', max_length=30, blank=True)
    email = models.EmailField(u'email', unique=True, null=True, blank=True)
    is_staff = models.BooleanField(u'职员状态', default=False, help_text='是否能够登录管理后台')
    is_active = models.BooleanField(u'是否激活', default=True, help_text='用户是否被激活，未激活则不能使用')
    date_joined = models.DateTimeField(u'创建日期', auto_now_add=True)
    avatar_url = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default_big.png', max_length=200,
                                   blank=True, null=True, verbose_name=u'头像220x220')
    avatar_middle_thumbnall = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default_middle.png',
                                                max_length=200, blank=True, null=True, verbose_name=u'头像104x104')
    avatar_small_thumbnall = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default_small.png',
                                               max_length=200, blank=True, null=True, verbose_name=u'头像70x70')
    avatar_alt = models.CharField(u'头像ALT说明', max_length=100, blank=True, null=True)
    qq = models.CharField(u'QQ号码', max_length=20, blank=True, null=True)
    mobile = models.CharField(u'手机号码', max_length=11, blank=True, null=True, unique=True)
    valid_email = models.SmallIntegerField(u'是否验证邮箱', default=0, choices=((0, u'否'), (1, u'是'),))
    company_name = models.CharField(u'公司名', max_length=150, blank=True, null=True)
    position = models.CharField(u'职位名', max_length=150, blank=True, null=True)
    description = models.TextField(u'个人介绍', blank=True, null=True)
    city = models.CharField(u'城市', max_length=30, null=True, blank=True)
    province = models.CharField(u'省份', max_length=30, null=True, blank=True)
    index = models.IntegerField(u'排列顺序(从小到大)', default=999)
    mylesson = models.ManyToManyField(Lesson, through=u'UserLearningLesson', verbose_name=u'我的学习章节')
    mystage = models.ManyToManyField(Stage, through=u'UserUnlockStage', verbose_name=u'我的解锁阶段')
    myfavorite = models.ManyToManyField(Course, through=u'MyFavorite', verbose_name=u'我的收藏')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        db_table = 'user_profile'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        'Returns the short name for the user.'
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 是否是老师
    def is_teacher(self):
        if self.groups.filter(name='老师').count() > 0:
            return True
        return False

    # 是否是学生
    def is_student(self):
        if self.groups.filter(name='学生').count() > 0:
            return True
        return False

    def __unicode__(self):
        return self.username


class MyCourse(models.Model):
    '''
    我的课程
    '''

    user = models.ForeignKey(UserProfile, related_name=u'mc_user', verbose_name=u'用户')
    course = models.CharField(u'课程ID', max_length=10)
    course_type = models.SmallIntegerField(u'课程类型', choices=((1, u'课程'), (2, u'职业课程'),))
    index = models.IntegerField(u'课程显示顺序(从小到大)', default=999)
    date_add = models.DateTimeField(u'添加时间', auto_now_add=True)

    class Meta:
        verbose_name = u'我的课程'
        verbose_name_plural = verbose_name
        db_table = 'my_course'

    def __unicode__(self):
        return str(self.id)


class MyFavorite(models.Model):
    '''
    我的收藏
    '''

    user = models.ForeignKey(UserProfile, related_name='mf_user', verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    date_favorite = models.DateTimeField(u'收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = u'我的收藏'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'course'),)
        db_table = 'my_favorite'

    def __unicode__(self):
        return str(self.id)


class UserLearningLesson(models.Model):
    '''
    用户学习章节记录(我的章节)
    '''

    date_learning = models.DateTimeField(u'最近学习时间', auto_now=True)
    is_complete = models.BooleanField(u'是否完成观看', default=False)
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')

    class Meta:
        verbose_name = u'我的章节'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'lesson'),)
        db_table = 'user_learning_lesson'

    def __unicode__(self):
        return str(self.id)


class UserUnlockStage(models.Model):
    '''
    用户解锁的具体阶段
    '''

    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    stage = models.ForeignKey(Stage, null=True, blank=True, verbose_name=u'解锁的阶段')
    date_unlock = models.DateTimeField(u'解锁时间', auto_now_add=True)

    class Meta:
        verbose_name = u'我的解锁阶段'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'stage'),)
        db_table = 'user_unlock_stage'

    def __unicode__(self):
        return str(self.id)


class Class(models.Model):
    '''
    班级
    '''

    coding = models.CharField(u'班级编号', unique=True, max_length=30)
    date_publish = models.DateTimeField(u'创建日期', auto_now_add=True)
    date_open = models.DateTimeField(u'开课日期')
    student_limit = models.IntegerField(u'学生上限', default=25)
    current_student_count = models.IntegerField(u'当前报名数', default=0)
    is_active = models.BooleanField(u'有效性', default=True)
    status = models.SmallIntegerField(u'班级状态', default=1, choices=((1, u'进行中'), (2, u'已结束'),))
    qq = models.CharField(u'班级QQ群', max_length=13)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher',
                                null=True, blank=True, verbose_name=u'班级老师')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students',
                                      through='ClassStudents', verbose_name=u'班级学生')
    career_course = models.ForeignKey(CareerCourse, verbose_name=u'职业课程')

    class Meta:
        verbose_name = u'班级'
        verbose_name_plural = verbose_name
        db_table = 'class'

    def __unicode__(self):
        return str(self.coding)


class ClassStudents(models.Model):
    '''
    班级和学生产生的关联对象
    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'学生')
    student_class = models.ForeignKey(Class, verbose_name=u'班级')
    study_point = models.IntegerField(u'学生在该班级下的学力', default=0)
    pause_reason = models.CharField(u'暂停原因', null=True, blank=True, max_length=200)
    pause_datetime = models.DateTimeField(u'暂停时间', null=True, blank=True, default=None)

    class Meta:
        verbose_name = u'班级学生'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'student_class'),)
        ordering = ['-study_point']
        db_table = 'class_students'

    def __unicode__(self):
        return str(self.id)


class Discuss(models.Model):
    '''
    章节讨论
    '''

    content = models.TextField(u'讨论内容')
    parent_id = models.IntegerField(u'父讨论ID', blank=True, null=True)
    date_publish = models.DateTimeField(u'发布时间', auto_now_add=True)
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    user_class = models.ForeignKey(Class, null=True, blank=True, verbose_name=u'班级')

    class Meta:
        verbose_name = '课程讨论'
        verbose_name_plural = verbose_name
        db_table = 'discuss'

    def __unicode__(self):
        return str(self.id)


class UserPurchase(models.Model):
    '''
    支付订单
    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    pay_price = models.IntegerField(u'金额')
    order_no = models.CharField(u'订单号', max_length=100, unique=True)
    trade_no = models.CharField(u'交易号', max_length=100, unique=True, null=True, blank=True)
    pay_type = models.SmallIntegerField(u'支付类型', choices=((0, u'全款'), (1, u'试学首付款'), (2, u'尾款'),
                                                          (3, u'阶段款')), default=0)
    date_add = models.DateTimeField(u'下单时间', auto_now_add=True)
    date_pay = models.DateTimeField(u'支付时间', null=True, blank=True)
    pay_way = models.SmallIntegerField(u'支付方式', choices=((1, u'网页支付宝'), (2, u'移动支付宝'),), )
    pay_status = models.SmallIntegerField(u'支付状态', null=True, blank=True, default=0,
                                          choices=((0, u'未支付'), (1, u'支付成功'), (2, u'支付失败'),), )
    pay_careercourse = models.ForeignKey(CareerCourse, verbose_name=u'支付订单对应职业课程')
    pay_class = models.ForeignKey(Class, verbose_name=u'支付订单对应班级号')
    pay_stage = models.ManyToManyField(Stage, verbose_name=u'支付订单对应阶段')

    class Meta:
        verbose_name = u'订单'
        verbose_name_plural = verbose_name
        db_table = 'user_purchase'

    def __unicode__(self):
        return self.order_no
