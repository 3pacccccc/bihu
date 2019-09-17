from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from qa.forms import QuestionForm
from qa.models import Question


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