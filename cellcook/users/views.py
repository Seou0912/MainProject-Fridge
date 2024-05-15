from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import User
from .validators import CustomPasswordValidator
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken


def fridge_main(request):
    if request.user.is_authenticated:
        return render(request, "fridge-main.html")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        vegetarian = request.POST.get("vegetarian", False)

        # 패스워드 검증
        validator = CustomPasswordValidator()
        try:
            validator.validate(password)
        except ValidationError as e:
            return render(request, "signup.html", {"error": str(e)})

        if password and confirm_password and password == confirm_password:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                nickname=nickname,
                vegetarian=vegetarian,
            )
            login(request, user)
            tokens = get_tokens_for_user(user)
            # 사용자를 바로 로그인 시킴
            return redirect("fridge-main")  # 성공 시 fridge-main 페이지로 리디렉션
        else:
            # return redirect('fridge')  # 성공 시 fridge 페이지로 리디렉션
            return render(
                request, "signup.html", {"error": "Password mismatch or missing fields"}
            )
    else:
        return render(request, "signup.html", {"error": "Invalid request"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("fridge-main")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("fridge")
        else:
            return render(request, "login.html", {"error": "Invalid login"})
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)

    return redirect("/")
