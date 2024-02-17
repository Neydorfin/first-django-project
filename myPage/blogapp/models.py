from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk}.{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f"{self.pk}.{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.pk}.{self.name}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk}.{self.title}"