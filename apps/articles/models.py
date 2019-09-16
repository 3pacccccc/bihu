from django.db import models
from django.db.models import Count
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from slugify import slugify
from taggit.managers import TaggableManager

from users.models import User


class ArticleQueryset(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_published(self):
        return self.filter(status='p')

    def get_drafts(self):
        return self.filter(status='D')

    def get_counted_tags(self):
        tag_ditc = {}
        query = self.filter(status='p').annotate(tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_ditc:
                    tag_ditc[tag] = 1
                else:
                    tag_ditc[tag] += 1
        return tag_ditc.items()


class Article(models.Model):
    STATUS = (('D', 'Draft'), ('P', 'Published'))

    title = models.CharField(max_length=255, null=False, unique=True, verbose_name='标题')
    user = models.ForeignKey(User, null=True, related_name='author', on_delete=models.SET_NULL, verbose_name="作者")
    image = models.ImageField(upload_to='articles/%Y/%m/%d/', verbose_name='文章图片')
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='动态')
    content = MarkdownxField(verbose_name='内容')
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = ArticleQueryset.as_manager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug = slugify(self.title)
            super(Article, self).save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)
