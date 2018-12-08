from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_OF_BLOGS_NUMBER)  # 每8页进行分页
    page_num = request.GET.get('page', 1)  # 获取页码参数 get请求
    page_of_blogs = paginator.get_page(page_num)  # 自动返回页面 如果为非数字，django会自动转换
    current_page_num = page_of_blogs.number  # 获取当前页码
    current_page_range = [x for x in range(int(current_page_num) - 2, int(current_page_num) + 3) if
                          0 < x <= paginator.num_pages]  # 根据当前页码确定显示的上下2页
    # print(current_page_range)  #[16, 17, 18, 19],[17, 18, 19],[1,2,3]
    # 加上省略标记         [ ...,5,6,7,8,9,... ]   ->   [1,...,5,6,7,8,9,...,end]
    if current_page_range[0] - 1 > 1:
        current_page_range.insert(0, '...')
    if paginator.num_pages - current_page_range[-1] > 1:
        current_page_range.append('...')
    # 判断列表中不存在首页和尾页 则添加  [1,...,5,6,7,8,9,...,end]
    if current_page_range[0] != 1:
        current_page_range.insert(0, 1)
    if current_page_range[-1] != paginator.num_pages:
        current_page_range.append(paginator.num_pages)

    # 获取博客分类对应的数量

    context = {}
    context['blogs'] = page_of_blogs.object_list  # 返回本页中的blog对象
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()  # 首页需要按照类型分类
    blog_date_dict = {}
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_count
    context['blog_dates'] = blog_date_dict  # 首页需要展示按照时间日期分类  {日期:博客数量，。。。}
    context['current_page_range'] = current_page_range  # 当前页的取值list
    # 返回blog中的全部博客，然后计算数目 也可以使用框架的方法{{ blogs |length }} 直接计算
    # context['blogs_count'] = Blog.objects.all().count()
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_with_type(request, blog_type_pk):
    # 得到一个BlogType中的一个类型
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_date.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()

    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response
