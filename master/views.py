from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *
from user.models import *
import random
from .pattern import Pattern
from .wrong_admin import *


# Create your views here.

def redirects(request, text, url):
    # 构建基于当前请求的完整 URL
    full_url = request.build_absolute_uri(url)
    # 使用构建的 URL 创建 HTML 链接
    html = f'<a href="{full_url}">{text}</a>'
    return HttpResponse(html)

# 首页
def index(request):
    user_id = request.session.get('user_id', False)
    # print(user_id)
    if user_id:
        user = UserInformation.objects.get(id=user_id)
        print(f'username:{user.username},user_id:{user_id}')
    else:
        return HttpResponseRedirect(reverse('user:login'))
    return render(request, 'master/index.html', locals())

def turn_next_group(request):
    print('turn to next group')
    return HttpResponseRedirect(reverse('master:pattern', args=['error']))
def end_review(request):
    if request.session.get('next_wrong_points'):
        del request.session['next_wrong_points']
    if request.session.get('history_id_error'):
        del request.session['history_id_error']
    return HttpResponseRedirect(reverse('user:personal'))

# 题目展示以及讲解入口
def turn_next_topic(request, next_topic, n_id, pattern, var_h, var_n):
    # 选择正确，那么应该跳转到下一题
    print('选择正确')
    if next_topic:
        print('进入历史题目下一题')
        return HttpResponseRedirect(reverse('master:topic_view', args=[n_id]))

    next_id = request.session.get(var_n, False)
    if next_id:
        return HttpResponseRedirect(reverse('master:pattern', args=[pattern]))
    else:
        # if request.session.get('pattern') != 'error' or not request.session.get('group', False):

        wrong_point_id = request.session.get('error_note', False)
        if wrong_point_id:
            if isinstance(wrong_point_id, list):# 复习模式
                print('review pattern')
                for i in wrong_point_id:
                    add_wrong_level(request, i)

                if request.session.get('next_wrong_points', False): # 跳转下一组
                    # 跳转选择是否下一组
                    next_group = True
                else:
                    next_group = False
                return render(request, 'master/hint.html', locals())

            else: # 单纯的错题本刷题
                print('from error note')
                add_wrong_level(request, wrong_point_id)

            return redirects(request, '恭喜你，这个知识点的错题复习完成', '/user/personal_center')
        print('delete history id and pattern')
        del request.session[var_h]
        del request.session['pattern']

        return redirects(request, '恭喜你，刷题完成', '/master/index')


def topic_view(request, topic_id):
    finished = True
    topic = get_object_or_404(Topic, id=topic_id)
    pattern = request.session.get('pattern', False)

    var_h = 'history_id' + '_' + pattern
    var_n = 'next_id' + '_' + pattern

    history_id = request.session.get(var_h, False)
    if not history_id:
        print(f'没有{var_h}')
        del request.session[var_n]
        return redirects(request, '请通过模式选择进入', '/master/index')

    end_id = history_id[-1]  # 为了看历史题目时，不出现提交按钮
    topic_index = history_id.index(topic_id)
    last_index = topic_index - 1
    next_index = topic_index + 1

    try:
        last_id = history_id[last_index]
        last_topic = False if topic_index == 0 else True
    except:
        last_topic = False
    try:
        n_id = history_id[next_index]
        next_topic = True
    except:
        next_topic = False
        n_id = 0

    if request.method == 'GET':
        if topic.type == 'w':
            select_id = topic.selections_set.first().id
        return render(request, 'master/topic.html', locals())

    elif request.method == 'POST':
        response = request.POST
        show_id = []  # 需要显示"跳转讲解部分"的选项id
        if topic.type == 'w':
            return turn_next_topic(request, next_topic, n_id, pattern, var_h, var_n)

        elif len(response) != len(topic.selections_set.all()):
            finished = False
            return render(request, 'master/topic.html', locals())
        else:  # 有选择选项，则判断正误
            for select_id, value in response.items():
                select = get_object_or_404(Selections, id=select_id)  # 获取这个选项

                if topic.type == 's':
                    va = bool(0) if value == 'False' else bool(1)
                    # 选择错误
                    show_id.append(int(select_id)) if va != select.judge else None
                    print(f'va:{va},judge:{select.judge}, {va != select.judge}')
                elif topic.type == 'c':
                    show_id.append(int(select_id)) if value != select.fill else None
                    print(f'va:{value},judge:{select.fill}, {value != select.fill}')

            if show_id:
                print(f'选项{show_id}选择错误')
                return render(request, 'master/explain_tran.html', locals())

            else:
                return turn_next_topic(request, next_topic, n_id, pattern, var_h, var_n)


# 题目跳转模式
def pattern(request, pattern):
    request.session['pattern'] = pattern
    run_pattern = Pattern(request)
    if pattern == 'random':
        return run_pattern.random()
    elif pattern == 'text':
        return run_pattern.text()
    elif pattern == 'knowledge_index':
        return run_pattern.knowledge_index()
    elif pattern == 'chapter_index':
        return run_pattern.chapter_index()
    elif pattern == 'knowledge':
        return run_pattern.knowledge()
    elif pattern == 'chapter':
        return run_pattern.chapter()
    elif pattern == 'error':
        return run_pattern.error()


def knowledge(request):  # 选项讲解
    select_id = request.GET.get('select_id')
    select = Selections.objects.filter(id=select_id)[0]
    points = Selections.objects.get(id=select_id).knowledgepoints_set.all()
    try:
        return render(request, f'master/explains/explain{select_id}.html', locals())
    except:
        return render(request, 'master/knowledge.html', locals())


def knowledge_explain(request, point_id):  # 知识点讲解

    points = KnowledgePoints.objects.filter(id=point_id)
    user_id = request.session.get('user_id')
    if user_id:
        add_wrong_topic(point_id, request.session['user_id'])

    return render(request, 'master/knowledge_explain.html', locals())


def w_explain(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Exception as e:
        return HttpResponse(f'没有这个topic_id，因为{e}')
    select_id = topic.selections_set.all()[0].id
    points = Selections.objects.get(id=select_id).knowledgepoints_set.all()
    return render(request, f'master/explain-w/explain{select_id}.html', locals())
