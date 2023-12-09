from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from master.models import Topic, Selections
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.
def divide_topicAndSelect(request):
    topics = []
    selects = []

    post = request.POST.copy()
    file = request.FILES.copy()
    response = {**post, **file}

    for key, value in response.items():
        if key.startswith("topic") and value:
            topics.append([key, value[0]])
        if key.startswith("select") and value:
            selects.append([key, value[0]])

    # 排序
    topics_sorted = sorted(topics, key=lambda x: x[0])
    if len(selects) == 1 and selects[0][1] == '':
        selects_sorted = None
    else:
        selects_sorted = sorted(selects, key=lambda x: x[0])

    return topics_sorted, selects_sorted


def create_topic(topic_date, type):
    new_topic = Topic()
    topic_value = ""
    for i in topic_date:
        if isinstance(i[-1], InMemoryUploadedFile):
            value = f"<br><img src='/media/image/{i[-1].name}'><br>"
            new_topic.photo = i[-1]
        else:
            value = f"<span>{i[-1]}</span>"
        topic_value += value
    new_topic.topic = topic_value
    new_topic.type = type
    new_topic.save()
    return new_topic


def divide_select(selects):
    select = {}
    for i in selects:
        key = i[0]
        select_num = key[6]
        text_num = key[7:]
        if i[-1]:
            # 先建选项
            select_title = 'select' + select_num
            if select_title not in select.keys():
                select[select_title] = {}

            # 再添加选项内容标题
            text_title = 'text' + text_num
            if text_title not in select[select_title].keys():
                select[select_title][text_title] = None

            # 最后添加选项内容值
            select[select_title][text_title] = i[-1]

    return select


def create_select(select_date, topic):
    # select_date = {'text0': '选项1', 'text1': '1680337359723.png', 'text2': '选项后'}
    new_select = Selections()
    new_select.select = 'default'
    new_select.topic_id = topic.id
    new_select.save()
    if select_date:
        select_value = ""
        for value in select_date.values():
            if isinstance(value, InMemoryUploadedFile):
                select_value += f"<br><img src='/media/image/{value.name}'><br>"
                new_select.select2 = value
            else:
                if 'type="text"' in value:
                    value = value.replace('type="text"', f'type="text" name="{new_select.id}"')
                if 'size=' in value:
                    text = value.split()
                    t_index = -1  # 初始化索引
                    for t in text:
                        if 'size' in t:
                            t_index = text.index(t)
                            break  # 找到后立即退出循环
                    if t_index != -1:  # 确保找到了包含 'size' 的元素
                        size_str = text[t_index]
                        size_list = size_str.split('=')
                        if len(size_list) > 1:
                            size = size_list[1]
                            try:
                                int(size)  # 尝试将 size 转换为整数
                            except ValueError:  # 捕获转换错误
                                value = value.replace(size_str, 'size="6"')  # 替换操作
                select_value += f"<span>{value}</span>"
        new_select.select = select_value
    else:
        new_select.select = str(topic.id) + '的选项'
    new_select.save()


"""run"""


def topic_input(request):
    type = request.GET.get('type')
    if request.method == "GET":
        return render(request, 'topic_input.html', {'type': type})
    else:
        source_date = divide_topicAndSelect(request)
        topics_sorted = source_date[0]
        print(f"分离后的topic：{topics_sorted}")
        selects_sorted = source_date[1]
        print(f"分离后的select：{selects_sorted}")

        topic = create_topic(topics_sorted, type)
        print("成功创建题目")

        # selects_sorted = [['select10', '选项1'], ['select11', '1680337359723.png'], ['select12', '选项后'], ['select20', '']]
        if selects_sorted:
            selects = divide_select(selects_sorted)
            print("成功分离选项")
            for key, value in selects.items():
                create_select(value, topic)
                print(f"成功创建选项：{key}")
        else:
            create_select(None, topic)

        return render(request, 'interact/topic.html', {'topic': topic, 'next_index': 1})
