# -*- coding: utf-8 -*-
from qa.models import Question


def vote_display(request):
    # 进入问题详情页后展示投票情况
    path = request.path
    question_id = int(path.split('/')[-2])
    question_obj = Question.objects.get(pk=question_id)
    try:
        vote_value = question_obj.votes.model.objects.get(user=request.user, object_id=question_id).value
    except Exception as e:
        vote_value = 'neutral'
    if vote_value is True:
        vote_value = 'up'
    elif vote_value is False:
        vote_value = 'down'

    return vote_value
