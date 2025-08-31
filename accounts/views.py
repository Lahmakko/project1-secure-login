from django.shortcuts import render
from django.http import HttpResponse
from .models import InsecureUser
# from django_ratelimit.decorators import ratelimit # For for Flaw 3
# from django.http import HttpResponseForbidden #For Flaw 3
#from django.contrib.auth.hashers import make_password, check_password  # FIX for flaw 3 + 5
# from django.contrib.auth.decorators import login_required  # FIX for flaw 4
#from django.contrib.auth.hashers import make_password #FIX for Flaw 5

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Flaw 1 + 5: passwords stored in plain text (no hashing/crypto)
        # hashed_pw = make_password(password)  # FIX commented out
        # InsecureUser.objects.create(username=username, password=hashed_pw)  # FIX commented out

        # Vulnerable version: still stores plaintext
        InsecureUser.objects.create(username=username, password=password)  # still plain text for 
        # flaw
        # Flaw 2: no input validation → injection risk
        # FIX: validate username/password, e.g., allowed characters only
        # if not username.isalnum():
        #     return HttpResponse("Invalid username: only letters and numbers allowed")
        # if len(password) < 8:
        #     return HttpResponse("Password too short")
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
            # Flaw 5: raw ORM query + plaintext password comparison
            user = InsecureUser.objects.get(username=username, password=password)
            #request.session['user_id'] = user.id  # Flaw 4 fix
            #request.session['username'] = user.username #Flaw 4 fix

            return HttpResponse(f"Welcome {username}! <a href='/login'>Back</a>")
        except InsecureUser.DoesNotExist:
            return HttpResponse("Login failed <a href='/login'>Try again</a>")
    return render(request, "accounts/login.html")





# Flaw 4: protected page

def secret_page(request):
    # Flaw 4: no login check, anyone can access
    # Commenting out the session check for demo:
    # if 'user_id' not in request.session:
    #     return HttpResponse("You must log in to see this page!")

    # The message itself stays so anyone visiting sees it:
    return HttpResponse("This is a secret page! Anyone can access it due to Flaw 4.")
