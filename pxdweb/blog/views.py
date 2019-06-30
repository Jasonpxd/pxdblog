from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Blog,BlogType
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read
from datetime import datetime
from comment.models import Comment
from comment.forms import CommentForm


def get_blog_list_common_date(blogs_all_list,request):
    paginator = Paginator(blogs_all_list, 5)  # 每10项作为一页进行分页
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    if paginator.num_pages < 7:
        page_range = [i for i in range(1, paginator.num_pages + 1)]
    else:
        if paginator.num_pages - 1 > current_page_num > 2:
            page_range = [current_page_num + i for i in range(-2, 5)]
        elif current_page_num <= 2:
            page_range = [i for i in range(1, 8)]
        elif current_page_num > page_of_blogs.paginator.num_pages - 2:
            page_range = [i for i in range(paginator.num_pages - 6, paginator.num_pages + 1)]
        # 前段的省略页码标记
        if page_range[0] - 1 >= 2:
            page_range[0] = '...'
        # 后段的省略页码标记
        if paginator.num_pages - page_range[-1] >= 2:
            page_range[-1] = '...'
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)
    blog_dates = Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_date(blogs_all_list,request)
    return render(request,'blog_list.html', context)

def blog_detail(request, blog_pk):
    blog =  get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)

    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['comments'] = comments.order_by('-comment_time')
    context['comment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id':blog_pk, 'reply_comment_id':0})
    response = render(request,'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response

def blog_with_type(request,blog_with_type):
    blog_type = get_object_or_404(BlogType,pk=blog_with_type)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_date(blogs_all_list, request)

    context['blog_type'] =blog_type
    return render(request,'blog_with_type.html',context)

def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_date(blogs_all_list, request)
    context['blog_date'] = str(year)+'年'+str(month)+'月'
    return render(request,'blog_with_date.html', context)