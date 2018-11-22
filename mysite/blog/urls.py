from django.urls import path
from .import views

#app_name = 'blog'
urlpatterns = [
    path('',views.blog_list,name='blog_list')
    #连接到文章
    ,path('<int:blog_pk>/', views.blog_detail, name='blog_detail')
    #连接到按照类型分类的页面
    ,path('type/<int:blog_type_pk>/',views.blog_with_type, name ='blog_with_type')
    #连接按照日期分类的页面
    ,path('date/<int:year>/<int:month>',views.blog_with_date,name='blog_with_date')
    ,
]
