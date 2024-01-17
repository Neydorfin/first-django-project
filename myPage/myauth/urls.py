from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    IndexView, 
    MyLogoutView,
    cookie_get_view,
    cookie_set_view,
    session_get_view,
    session_set_view,
    )


app_name = "myauth"
urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
            ),
    name="login"),

    path("", IndexView.as_view(), name="index"),
    path("logout/", MyLogoutView.as_view(), name="logout"),

    path("cookie/get/", cookie_get_view, name="cookie_get"),
    path("cookie/set/", cookie_set_view, name="cookie_set"),
    path("session/get/", session_get_view, name="session_get"),
    path("session/set/", session_set_view, name="session_set"),
]
