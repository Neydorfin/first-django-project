from django.db import models
from django.utils.translation import gettext_lazy, ngettext_lazy


class Author(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Author")
        verbose_name_plural = gettext_lazy("Authors")
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk}.{self.name}"


class Category(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Category")
        verbose_name_plural = gettext_lazy("Categories")
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f"{self.pk}.{self.name}"


class Tag(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Tag")
        verbose_name_plural = gettext_lazy("Tags")
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.pk}.{self.name}"


class Article(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Article")
        verbose_name_plural = gettext_lazy("Articles")
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk}.{self.title}"