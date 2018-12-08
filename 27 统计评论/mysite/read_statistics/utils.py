import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistics_once_read(request, obj):
    '''此方法用于判断cookie中的阅读计数是否存在，没有则计数加1，并返回生成的key，
        没有说明cookie存在，不做阅读计数，当cookie失效时才去做统计计数加一，
        在视图函数中，默认设置cookie时长为浏览器关闭则cookie失效，
        cookie的设置是在用户访问具体的视图函数时添加的'''
    ct = ContentType.objects.get_for_model(obj)  # 通过具体的obj【记录】获取contentType中的对应的model【表/类】
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 总阅读数加1
        readnum, bool = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        # 当天阅读数加1
        date = timezone.now().date()
        readDetail, bool = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


def get_seven_days_read_data(content_type):
    '''此方法传入一个content_type对象 即具体的某个模型
    得到前七天的日期及阅读计数 列表 -7- -1'''
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result_dict = read_detail.aggregate(read_num_sum=Sum('read_num'))  # 聚合返回read_num列的计数 得到字典{read_num_sum:sum()}
        read_nums.append(result_dict['read_num_sum'] or 0)  # 添加统计结果 none则0
    return dates, read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]


def get_7days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    #关联查询 跨表查询 聚合  通过阅读日期计数表 关联的contenttype获取blog表中的对象
    #content_type确定某个表和其关联
    read_details = ReadDetail.objects \
        .filter(content_type=content_type, date__lt=today, date__gte=date) \
        .values('content_type', 'object_id') \
        .annotate(read_num_sum=Sum('read_num')) \
        .order_by('-read_num_sum')
    return read_details[:7]
