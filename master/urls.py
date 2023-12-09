from django.urls import path
from . import views
from .views import *


app_name = 'master'
urlpatterns = [

    # 知识讲解
    path('knowledge', views.knowledge, name='knowledge'),
    path('knowledge/<int:select_id>', views.knowledge),
    path('knowledge_explain/<int:point_id>', views.knowledge_explain, name='explain'),
    # 刷题模式选择
    path('index', views.index, name='index'),
    # 每个题目单独页面
    path('topic/<int:topic_id>', views.topic_view, name='topic_view'),
    # 题目模式
    path('pattern/<str:pattern>', views.pattern, name='pattern'),
    # path('pattern/<str:pattern>/<int:know_pid>', views.pattern, name='pattern_withpid'),
    # w（主观题）的题目讲解
    path('w_explain/<int:topic_id>', views.w_explain, name='w_explain'),
    # 跳转下一组
    path('next_group', views.turn_next_group, name='next_group'),
    # 结束复习
    path('end_review', views.end_review, name='end_review')

]