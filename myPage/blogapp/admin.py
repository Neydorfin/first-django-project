from typing import Any
from django.contrib import admin
from blogapp.models import Article, Tag, Category, Author
from django.db.models.query import QuerySet
from django.http import HttpRequest


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "bio_short",
    )
    list_display_links = (
        "pk",
        "name",
    )
    ordering = ("pk",)
    search_fields = (
        "pk",
        "name",
    )

    def bio_short(self, obj: Article) -> str:
        if len(obj.bio) > 48:
            return obj.bio[:48] + "..."
        return obj.bio


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    list_display_links = (
        "pk",
        "name",
    )
    ordering = ("pk",)
    search_fields = (
        "pk",
        "name",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    list_display_links = (
        "pk",
        "name",
    )
    ordering = ("pk",)
    search_fields = (
        "pk",
        "name",
    )


class TagInline(admin.StackedInline):
    model = Article.tags.through


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]
    list_display = (
        "pk",
        "title",
        "author_name",
        "content_short",
        "category",
        "pub_date",
    )
    list_display_links = (
        "pk",
        "title",
        "author_name",
    )
    ordering = ("pk",)
    search_fields = (
        "pk",
        "name",
        "category",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Article.objects.select_related("author").select_related("category").prefetch_related("tags")

    def author_name(self, obj: Article) -> str:
        return obj.author.name

    def content_short(self, obj: Article) -> str:
        if len(obj.content) > 48:
            return obj.content[:48] + "..."
        return obj.content
