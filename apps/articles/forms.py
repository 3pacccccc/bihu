# -*- coding: utf-8 -*-
from django import forms
from markdownx.fields import MarkdownxFormField

from articles.models import Article


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())  # 隐藏
    edited = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)
    content = MarkdownxFormField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'tags', 'status', 'edited']
