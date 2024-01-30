from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    ProfileListView, 
    ProfileDetailView, 
    MyLogoutView,
    RegisterView,


    cookie_get_view,
    cookie_set_view,
    session_get_view,
    session_set_view,
    )


app_name = "accounts"
urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
            ),
    name="login"),

    path("", ProfileListView.as_view(), name="profile_list"),
    path("<username>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    path("cookie/get/", cookie_get_view, name="cookie_get"),
    path("cookie/set/", cookie_set_view, name="cookie_set"),
    path("session/get/", session_get_view, name="session_get"),
    path("session/set/", session_set_view, name="session_set"),
]
