#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from repository import models
from utils.pagination import Pagination
from django.urls import reverse
import json
from django.conf import settings
from django.http import JsonResponse
import os
import sys
import datetime as dt
import  uuid
def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """
    # return render(request,'index.html')
    # 获取文章类型
    article_type_list = models.Article.type_choices
    # {},[]
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs=kwargs)#   all/1.html
    else:
        article_type_id = None
        base_url = '/' # /

    data_count = models.Article.objects.filter(**kwargs).count()


    page_obj = Pagination(request.GET.get('p'),data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)

    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'page_str': page_str,
        }
    )


def home(request, site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/wupeiqi.html
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    article_list = models.Article.objects.filter(blog=blog).order_by('-nid').all()

    return render(
        request,
        'home.html',
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )


def filter(request, site, condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    template_name = "home_summary_list.html"
    if condition == 'tag':
        template_name = "home_title_list.html"
        article_list = models.Article.objects.filter(tags=val, blog=blog).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(category_id=val, blog=blog).all()
    elif condition == 'date':
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
    else:
        article_list = []

    return render(
        request,
        template_name,
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )


def detail(request, site, nid):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category', 'articledetail').first()
    comment_list = models.Comment.objects.filter(article=article).select_related('reply')


    return render(
        request,
        'home_detail.html',
        {
            'blog': blog,
            'article': article,
            'comment_list': comment_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
        }

    )


def upload_img(request, dir_name):
        ##################
        #  kindeditor图片上传返回数据格式说明：
        # {"error": 1, "message": "出错信息"}
        # {"error": 0, "url": "图片地址"}
        ##################
        result = {"error": 1, "message": "上传出错"}
        files = request.FILES.get("imgFile", None)
        if files:
            result = image_upload(files, dir_name)
        return HttpResponse(json.dumps(result), content_type="application/json")
    # 目录创建
def upload_generation_dir(dir_name):
        today = dt.datetime.today()
        dir_name = dir_name + '/%d/%d/' % (today.year, today.month)
        if not os.path.exists(settings.MEDIA_ROOT + dir_name):
            os.makedirs(settings.MEDIA_ROOT + dir_name)
        return dir_name

    # 图片上传

def image_upload(files, dir_name):

        # 允许上传文件类型

        allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']

        file_suffix = files.name.split(".")[-1]

        if file_suffix not in allow_suffix:
            return {"error": 1, "message": "图片格式不正确"}

        relative_path_file = upload_generation_dir(dir_name)

        path = os.path.join(settings.MEDIA_ROOT, relative_path_file)

        if not os.path.exists(path):  # 如果目录不存在创建目录

            os.makedirs(path)

        file_name = str(uuid.uuid1()) + "." + file_suffix

        path_file = os.path.join(path, file_name)

        file_url = settings.MEDIA_URL + relative_path_file + file_name

        open(path_file, 'wb').write(files.file.read())  # 保存图片

        return {"error": 0, "url": file_url}

