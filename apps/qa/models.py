from django.db import models
from markdownx.models import MarkdownxField
from slugify import slugify
from taggit.managers import TaggableManager

from users.models import User


class QuestionQuerySet(models.query.QuerySet):
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
    # votes = GenericRelation(Vote, verbose_name='投票情况')  # 通过GenericRelation关联到Vote表，不是实际的字段
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
