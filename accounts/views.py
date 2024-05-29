from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import FormView, CreateView, DeleteView, DetailView, ListView

from accounts.forms import LoginForm, RegisterForm
from accounts.models import ActivateToken
#from accounts.services import AccountsEmailNotification
from config import settings

User = get_user_model()


@login_required
def home_view(request: HttpRequest) -> HttpResponse:
    print(reverse("accounts:activate", args=['admin', 'user_token']))
    return render(request, "home.html")


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            return redirect("accounts:home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        user_token = ActivateToken.objects.create(user=user)

        activate_url = (
            f"{self.request.scheme}://{self.request.get_host()}"
            f'{reverse("accounts:activate", args=[user.username, user_token.token])}'
        )

        email_service = AccountsEmailNotification()
        email_service.send_activation_email(
            user.email, user.get_full_name(), activate_url
        )

        messages.info(
            self.request,
            "Registration completed. Please check your email to activate your account.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ActivateAccountView(View):
    def get(self, request: HttpRequest, username: str, token: str):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(ActivateToken, token=token, user=user)

        if user.is_active:
            token.delete()
            messages.error(request, "User is already activated")
            return redirect("accounts:home")

        if token.verify_token():
            user.is_active = True
            token.delete()
            user.save()

            messages.success(request, "Activation complete")
            return redirect("accounts:home")

        messages.error(request, "Token expired")
        return redirect("accounts:home")


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You're already logged in")
        return redirect("accounts:home")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(request, email=email, password=password)

            if not user:
                messages.error(request, "Invalid login or password")
                return redirect("accounts:login")

            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 7)
            else:
                request.session.set_expiry(0)

            login(request, user)

            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, settings.ALLOWED_HOSTS
            ):
                return redirect(iri_to_uri(next_url))

            return redirect("accounts:home")
        else:
            return render(request, "accounts/login.html", {"form": form})

    form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:home')
