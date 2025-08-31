from django.shortcuts import render
from django.http import HttpResponse
from .models import InsecureUser
# from django.contrib.auth.hashers import make_password, check_password  # FIX for flaw 3 + 5
# from django.contrib.auth.decorators import login_required            # FIX for flaw 4

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Flaw 1 + 5: passwords stored in plain text (no hashing/crypto)
        # FIX: hashed_pw = make_password(password)
        # InsecureUser.objects.create(username=username, password=hashed_pw)
        InsecureUser.objects.create(username=username, password=password)

        # Flaw 2: no input validation → injection risk
        # FIX: validate username/password, e.g., allowed characters only

        return HttpResponse(f"User {username} registered! <a href='/login'>Login</a>")
    return render(request, "accounts/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Flaw 2 + 5: raw ORM query + no hashing check → injection + crypto failure
            user = InsecureUser.objects.get(username=username, password=password)
            
            # Flaw 4: no session handling → broken authentication / access control
            # FIX: store user in session
            # request.session['user'] = user.id

            # Flaw 3: no brute-force / rate limiting
            # FIX: implement request throttling using a decorator or package like django-ratelimit

            return HttpResponse(f"Welcome {username}! <a href='/login'>Back</a>")
        except InsecureUser.DoesNotExist:
            return HttpResponse("Login failed <a href='/login'>Try again</a>")
    return render(request, "accounts/login.html")
