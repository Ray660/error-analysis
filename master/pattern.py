from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *
from user.models import *
import random


def pick_next_topic(request, next_id, topic_id, history_id, pattern):
    next_id.remove(topic_id)
    var_n = 'next_id' + '_' + pattern
    var_h = 'history_id' + '_' + pattern
    if topic_id in history_id:
        print('overlap of topic')
        if next_id:
            del request.session[var_n]
        if history_id:
            del request.session[var_h]
        return HttpResponseRedirect(reverse('master:index'))
    history_id.append(topic_id)
    request.session[var_h] = history_id
    print(f'目前的历史id：{request.session[var_h]}')

    if next_id:
        request.session[var_n] = next_id
        print(f'目前的待选id：{request.session[var_n]}')

    else:  # 题目做完了

        print(f"最后一道题的id：{topic_id}")

    return HttpResponseRedirect(f'/master/topic/{topic_id}')


def get_sessionid(request, pattern):
    var_n = 'next_id' + '_' + pattern
    var_h = 'history_id' + '_' + pattern

    next_id = request.session[var_n]
    history_id = request.session.get(var_h, False)
    if not history_id:
        print(f'出错，没有{var_h}')
        del request.session[var_n]
        if pattern == 'knowledge' or pattern == 'chapter':
            return HttpResponseRedirect(reverse('master:pattern', args=[f'{pattern}_index']))
        else:
            return HttpResponseRedirect(reverse('master:index'))

    return next_id, history_id


def update_next_wrong_points(request, next_wrong_points):
    if len(next_wrong_points) > 5:
        group = random.sample(next_wrong_points, 5)
    else:
        group = next_wrong_points

    next_wrong_points = [i for i in next_wrong_points if i not in group]

    print(f'create or update session: next_wrong_points{next_wrong_points}')
    request.session['next_wrong_points'] = next_wrong_points
    return group


def get_group(request):
    if not request.session.get('next_wrong_points', False):
        print('create next_wrong_points')
        user_id = request.session.get('user_id', False)
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))
        all_wrong_points = [point.wrong_pointid for point in
                            WrongQuestion.objects.filter(user_id=user_id, is_active=True).order_by('level_mastery',
                                                                                                   'edited_time')]
        next_wrong_points = all_wrong_points
        group = update_next_wrong_points(request, next_wrong_points)

    else:
        next_wrong_points = request.session.get('next_wrong_points')
        print(f'get next_wrong_points:{next_wrong_points}')
        group = update_next_wrong_points(request, next_wrong_points)

    print(f'get group:{group}')
    return group


class Pattern:

    def __init__(self, request):
        self.request = request

    def random(self):
        pattern = 'random'
        if not self.request.session.get('next_id_random', False):  # 首次做题
            all_topics = Topic.objects.all()
            next_id = [topic.id for topic in all_topics]  # 待选id集
            history_id = []  # 历史题目id集
        else:
            session_id = get_sessionid(self.request, pattern)
            next_id = session_id[0]
            history_id = session_id[1]

        topic_id = random.choice(next_id)

        return pick_next_topic(self.request, next_id, topic_id, history_id, pattern)

    def text(self):
        pattern = 'text'

        all_topics = Topic.objects.all()
        next_id = [topic.id for topic in all_topics]  # 待选id集
        history_id = []  # 历史题目id集

        topic_id = int(input('要测试的题目id：'))

        return pick_next_topic(self.request, next_id, topic_id, history_id, pattern)


def knowledge_index(self):
    pattern = 'knowledge_index'
    points = KnowledgePoints.objects.all()
    return render(self.request, 'master/knowledge_pattern.html', locals())


def chapter_index(self):
    pattern = 'chapter_index'
    edition = self.request.GET.get('edition', 'SE')
    return render(self.request, 'master/chapter_index.html', locals())


def knowledge(self):
    pattern = 'knowledge'
    if not self.request.session.get('next_id_knowledge', False) or self.request.GET.get('from') == 'error_note':  # 首次做题
        print('create next id and history id')
        point_id = self.request.GET['know_pid']
        point = KnowledgePoints.objects.get(id=point_id)
        selects = point.select.all()
        next_id0 = [select.topic.id for select in selects]  # 待选id集
        # 去除重复元素
        next_id = list(set(next_id0))
        if self.request.GET.get('from') == 'error_note':
            self.request.session['error_note'] = point_id
            print(f"create session error_note:{self.request.session['error_note']}")
            if len(next_id) > 3:
                choose_nid = random.sample(next_id, 3)
                next_id = choose_nid
        history_id = []  # 历史题目id集
    else:
        print('update next id and history id')
        session_id = get_sessionid(self.request, pattern)
        next_id = session_id[0]
        history_id = session_id[1]
    topic_id = random.choice(next_id)

    return pick_next_topic(self.request, next_id, topic_id, history_id, pattern)


def chapter(self):
    pattern = 'chapter'
    if not self.request.session.get('next_id_chapter', False):
        nodule = self.request.GET['nodule']
        print(type(nodule))

        points = KnowledgePoints.objects.filter(science_education_edition=nodule)
        if not points:
            url = reverse('master:pattern', args=['chapter_index'])
            html = f"<a href='{url}'>目前该章节还未收录题目，敬请期待</a>"
            return HttpResponse(html)

        selects = []
        for point in points:
            for s in point.select.all():
                selects.append(s)
        next_id0 = [select.topic.id for select in selects]
        next_id = list(set(next_id0))
        history_id = []
    else:
        session_id = get_sessionid(self.request, pattern)
        next_id = session_id[0]
        history_id = session_id[1]
    topic_id = random.choice(next_id)
    return pick_next_topic(self.request, next_id, topic_id, history_id, pattern)


def error(self):
    pattern = 'error'
    if not self.request.session.get('next_id_error', False):  # 首次做题
        group = get_group(self.request)
        next_ids = []
        for point_id in group:
            selects = KnowledgePoints.objects.get(id=point_id).select.all()
            next_id0 = [select.topic.id for select in selects]  # 待选id集
            # 去除重复元素
            next_id_one = list(set(next_id0))
            if len(next_id_one) > 3:
                choose_nid = random.sample(next_id_one, 3)
                next_id_one = choose_nid
            next_ids.extend(next_id_one)
        print('create next id')
        next_id = list(set(next_ids))

        self.request.session['error_note'] = [point_id for point_id in group]
        print(f"create session error_note(point_id):{self.request.session['error_note']}")

        if not self.request.session.get('history_id_error', False):
            print('create history id')
            history_id = []  # 历史题目id集
        else:
            print('get history id')
            history_id = self.request.session.get('history_id_error')
            # 保证next id 与 history id 不重合
            next_id = [i for i in next_id if i not in history_id]
            if not next_id:
                print('next id is none')
                if not self.request.session.get('next_wrong_points', False):  # 题目已全部复习完
                    print('the topic is over')
                    next_group = False
                    return render(self.request, 'master/hint.html', locals())
                else:  # 继续下一组选择
                    print('get next group')
                    return HttpResponseRedirect(reverse('master:pattern'), args=['error'])
    else:
        print('get next id and history id')
        session_id = get_sessionid(self.request, pattern)
        next_id = session_id[0]
        history_id = session_id[1]

    print('get topic id')
    topic_id = random.choice(next_id)

    return pick_next_topic(self.request, next_id, topic_id, history_id, pattern)
