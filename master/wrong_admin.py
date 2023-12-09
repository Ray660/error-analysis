from user.models import *
from django.db.models import F


def add_wrong_topic(point_id, user_id):
    point_id = int(point_id)
    wrong_point = WrongQuestion.objects.filter(wrong_pointid=point_id, user_id=user_id, point_id=point_id).first()
    if wrong_point is None:
        WrongQuestion.objects.create(wrong_pointid=point_id, user_id=user_id, point_id=point_id)

    else:
        if wrong_point.is_active == False:
            wrong_point.is_active = True
        level = wrong_point.level_mastery
        if level > 1:
            wrong_point.level_mastery = F('level_mastery') - 1
        else:
            wrong_point.level_mastery = 1
        wrong_point.save()


def add_wrong_level(request, wrong_point_id):
    user_id = request.session.get('user_id')

    wrong_point = WrongQuestion.objects.filter(wrong_pointid=wrong_point_id, user_id=user_id, is_active=True).first()
    if wrong_point is None:
        print(f"There are something errors in error_note")

    if wrong_point.level_mastery < 4:
        wrong_point.level_mastery = F('level_mastery') + 1
        wrong_point.save()
    else:
        wrong_point.is_active = False
        wrong_point.save()
