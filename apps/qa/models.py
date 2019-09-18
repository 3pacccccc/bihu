import uuid
from collections import Counter

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from slugify import slugify
from taggit.managers import TaggableManager

from users.models import User


class Vote(models.Model):
    uuid_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, related_name='qa_voter', on_delete=models.CASCADE)
    value = models.BooleanField(default=True, verbose_name='赞同或者反对')
    # GenericForeignKey设置
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='votes_on', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50, blank=True, null=True)
    vote = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class QuestionQuerySet(models.query.QuerySet):

    def get_answered(self):
        """已有回答的问题"""
        return self.filter(has_answer=True)

    def get_unanswered(self):
        """未被回答的问题"""
        return self.filter(has_answer=False)

    def get_counted_tags(self):
        """用字典的形式返回问题的标签和"""
        tag_dict = {}
        query = self.all().annotate(tagged=models.Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:
                    tag_dict[tag] += 1

        return tag_dict.items()


class Question(models.Model):
    STATUS = (("O", "Open"), ("C", "Closed"), ("D", "Draft"))
    user = models.ForeignKey(User, related_name='q_author', on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=200, unique=True, blank=False, verbose_name='标题')
    slug = models.SlugField(max_length=200, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(choices=STATUS, default='O', verbose_name='问题动态', max_length=10)
    content = MarkdownxField(verbose_name='问题内容')
    has_answer = models.BooleanField(default=False, verbose_name='接收回答')
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='标签')
    votes = GenericRelation(Vote, verbose_name='投票情况')  # 通过GenericRelation关联到Vote表，不是实际的字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def count_answers(self):
        return Answer.objects.filter(question=self).count()

    def total_votes(self):
        """得票数"""
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_answers(self):
        """问题的所有回答"""
        return Answer.objects.filter(question=self)

    def get_accepted_answer(self):
        """被接受的回答"""
        return Answer.objects.get(question=self, is_answer=True)

    def get_markdown(self):
        return markdownify(self.content)


class Answer(models.Model):
    uuid_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, related_name='a_author', on_delete=models.CASCADE, verbose_name='用户')
    question = models.ForeignKey(Question, related_name='question', verbose_name='问题', on_delete=models.CASCADE)
    content = MarkdownxField(verbose_name='回答内容')
    is_answer = models.BooleanField(default=False, verbose_name='是否为接受回答')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    votes = GenericRelation(Vote, verbose_name='投票情况')  # 通过GenericRelation关联到Vote表，不是实际的字段

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = verbose_name
        ordering = ['-is_answer', 'created_at']  # 多字段排序

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数"""
        dic = Counter(self.votes.values_list("value", flat=True))
        return dic[True] - dic[False]

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False)]

    def accept_answer(self):
        """接受回答"""
        # 当一个问题有多个回答的时候，只能接受一个回答，其它回答一律置为未接受
        answer_set = Answer.objects.filter(question=self.question)  # 查询当前问题的所有回答
        answer_set.update(is_answer=False)  # 一律置为未接受
        # 接受当前回答并保存
        self.is_answer = True
        self.save()
        # 该问题已有被接受的回答，保存
        self.question.has_answer = True
        self.question.save()
