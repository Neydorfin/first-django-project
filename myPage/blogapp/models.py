from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=40)


class Tag(models.Model):
    name = models.CharField(max_length=20)