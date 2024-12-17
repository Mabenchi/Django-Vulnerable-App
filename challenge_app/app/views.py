from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.contrib.auth.models import User

# Create your views here.

def search_members(request):
    if request.method == "GET":
        username = request.GET.get("username")

        # Vulnerable query without parameterization
        query = f"SELECT username,email,date_joined FROM auth_user WHERE username = '{username}'"  # SQL Injection risk
        try:
            # Execute raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(query)
                members = cursor.fetchall()
        except Exception as e:
            template = loader.get_template('search_members.html')
            return HttpResponse(template.render({'error_message': e}))
        # Display results
        return render(request, 'search_members.html', {'members': members})

    return render(request, 'search_members.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Vulnerability: No input validation
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return list_members(request)
        except Exception as e:
            template = loader.get_template('register.html')
            return HttpResponse(template.render({'error_message': e}))
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

def list_members(request):
    # Query all users XSS
    members = User.objects.all()
    return render(request, 'list_members.html', {'members': members})

def home_page(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
