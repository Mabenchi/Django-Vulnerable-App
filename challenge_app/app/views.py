from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User

# Create your views here.

def members(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Vulnerability: No input validation or duplicate user checks
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            # Vulnerability: Password stored without hashing if `make_password` is omitted
            user.save()
            return HttpResponse("User registered successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

def home_page(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
