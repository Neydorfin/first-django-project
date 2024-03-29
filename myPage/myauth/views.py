from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from .models import Profile
from .forms import ProfileForm


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "myauth/profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "myauth/profiles_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return Profile.objects.select_related("user").get(user=User.objects.get(username=self.kwargs["username"]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm()  # Ваша форма
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("accounts:profile_detail", kwargs={"username": profile.user.username}))
        else:
            return render(request, self.template_name, {'form': form, 'object': profile})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class RegisterView(CreateView):
    template_name = "myauth/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:profile_list")

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
