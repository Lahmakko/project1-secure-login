from django.shortcuts import render
from django.http import HttpResponse
from .models import InsecureUser
# from django_ratelimit.decorators import ratelimit
# from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password, check_password  # FIX for flaw 3 + 5
# from django.contrib.auth.decorators import login_required  # FIX for flaw 4

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Flaw 1 + 5: passwords stored in plain text (no hashing/crypto)
        # hashed_pw = make_password(password) #FIX for flaw 1
        # InsecureUser.objects.create(username=username, password=hashed_pw) #FIX for flaw 1

        # Flaw 2: no input validation → injection risk
        # FIX: validate username/password, e.g., allowed characters only
        # if not username.isalnum():
        #     return HttpResponse("Invalid username: only letters and numbers allowed")
        # if len(password) < 8:
        #     return HttpResponse("Password too short")

        # InsecureUser.objects.create(username=username, password=password)  # still plain text for flaw
        return HttpResponse(f"User {username} registered! <a href='/login'>Login</a>")
    return render(request, "accounts/register.html")


def login(request):
    # Flaw 3: rate limiting removed for demo
    # if getattr(request, 'limited', False):
    #     return HttpResponseForbidden("Too many login attempts. Try again later.")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Flaw 2 + 5: raw ORM query + no hashing check → injection + crypto failure
            user = InsecureUser.objects.get(username=username, password=password)
            
            # Flaw 4: no session handling → broken authentication / access control
            # Demo: no session is set, so even "logged in" users are not tracked
            # FIX would be: request.session['user_id'] = user.id

            return HttpResponse(f"Welcome {username}! <a href='/login'>Back</a>")
        except InsecureUser.DoesNotExist:
            return HttpResponse("Login failed <a href='/login'>Try again</a>")
    return render(request, "accounts/login.html")


# Flaw 4: protected page
def secret_page(request):
    # Flaw 4: no login check, anyone can access
    # FIX would be: check session key
    # if 'user_id' not in request.session:
    #     return HttpResponse("You must log in to see this page!")

    return HttpResponse("This is a secret page! Anyone can access it due to Flaw 4.")
