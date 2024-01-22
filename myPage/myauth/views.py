from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import Profile

class IndexView(TemplateView):
    template_name = "myauth/index.html"

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        # Check if user is authenticated
        if not self.request.user.is_authenticated:
            # Redirect them to the login page if not
            return redirect('accounts:login')
        else:
            return render(self.request, self.template_name)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class RegisterView(CreateView):
    template_name = "myauth/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response


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
