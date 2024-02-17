from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from blogapp.models import Article


class ArticleListView(ListView):
    queryset = Article.objects.select_related("author").select_related("category").prefetch_related("tags").defer("content")
    template_name = "blogapp/article_list.html"
    context_object_name = 'articles'
