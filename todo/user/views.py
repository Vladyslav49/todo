from http import HTTPMethod

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]


def user_register(request: HttpRequest) -> HttpResponse:
    if request.method == HTTPMethod.POST:
        form = RegisterForm(request.POST)  # type: ignore[var-annotated]

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})
