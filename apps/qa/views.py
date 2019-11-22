from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView

from notifications.views import notification_handler
from qa.forms import QuestionForm
from qa.models import Question, Answer
from utils.helper import ajax_require
from utils.qa_utils import vote_display


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    paginate_by = 10
    template_name = 'qa/question_list.html'
    context_object_name = 'questions'

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Question.objects.get_counted_tags()
        context['active'] = 'all'
        return context


class AnsweredQuestionsListView(QuestionListView):
    """
    已回答的问题
    """

    def get_queryset(self):
        return Question.objects.filter(has_answer=True)

    def get_context_data(self, *args, **kwargs):
        context = super(AnsweredQuestionsListView, self).get_context_data(*args, **kwargs)
        context['active'] = 'answered'
        return context


class UnansweredQuestionsListView(QuestionListView):
    """未回答的问题，继承自QuestionsListView"""

    def get_queryset(self, **kwargs):
        return Question.objects.filter(has_answer=False)

    def get_context_data(self, *args, **kwargs):
        context = super(UnansweredQuestionsListView, self).get_context_data(*args, **kwargs)
        context["active"] = "unanswered"
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """
    问题详情
    """
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        vote_value = vote_display(self.request)
        context['vote_value'] = vote_value
        return context


@method_decorator(cache_page(60 * 60), name='get')  # 将CreateArticleView GET方法返回的数据缓存
class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    提出问题
    """
    form_class = QuestionForm
    template_name = 'qa/question_form.html'
    message = "问题已提交！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:unanswered_q')


@method_decorator(cache_page(60 * 60), name='get')  # 将CreateArticleView GET方法返回的数据缓存
class CreateAnswerView(LoginRequiredMixin, CreateView):
    """
    回答问题
    """
    model = Answer
    fields = ['content', ]
    message = "您的问题已提交"
    template_name = 'qa/answer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:question_detail', kwargs={'pk': self.kwargs['question_id']})


@login_required
@ajax_require
@require_http_methods(["POST"])
def question_vote(request):
    """
    给问题投票， ajax请求
    :param request:
    :return:
    """
    question_id = request.POST.get('question', '')
    value = True if request.POST.get('value') == 'U' else False
    question = Question.objects.get(pk=int(question_id))
    users = question.votes.values_list('user', flat=True)
    if request.user.pk in users and value == question.votes.get(user=request.user).value:
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={'value': value})

    return JsonResponse({'votes': question.total_votes()})


@login_required
@ajax_require
@require_http_methods(["POST"])
def answer_vote(request):
    """
    给回答投票
    """
    answer_id = request.POST.get('answer', '')
    value = True if request.POST['value'] == 'U' else False
    answer = Answer.objects.get(uuid_id=answer_id)
    users = answer.votes.values_list('user', flat=True)

    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": answer.total_votes()})


@login_required
@ajax_require
@require_http_methods(["POST"])
def accept_answer(request):
    """
    接收回答，ajax post请求
    已经被接收的回答用户不能取消
    """
    answer_id = request.POST.get('answer', '')
    answer = Answer.objects.get(uuid_id=answer_id)
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    notification_handler(request.user, answer.user, 'W', answer)
    return JsonResponse({'status': 'true'}, status=200)
