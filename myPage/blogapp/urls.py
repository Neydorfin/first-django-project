from django.urls import path
from blogapp.views import ArticleListView

app_name = "blog"
urlpatterns = [
   path("", ArticleListView.as_view(), name="articles_list")
]
