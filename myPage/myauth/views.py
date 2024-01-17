from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "myauth/index.html"

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        # Check if user is authenticated
        if not self.request.user.is_authenticated:
            # Redirect them to the login page if not
            return redirect('myauth:login')
        else:
            return render(self.request, self.template_name)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def cookie_set_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set!")
    response.set_cookie("message", "HELLO", max_age=1800)
    return response


def cookie_get_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("message", None)
    if value:
        return HttpResponse(f"Cookie value: {value!r}")
    else:
        return HttpResponse("Cookie not seted!")

def session_set_view(request: HttpRequest) -> HttpResponse:
    request.session["message"] = "World"
    return HttpResponse("Session set!")


def session_get_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("message", None)
    if value:
        return HttpResponse(f"Session value: {value!r}")
    else:
        return HttpResponse("Session not seted!")