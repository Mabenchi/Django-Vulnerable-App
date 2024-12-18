from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Amount

# Create your views here.
@login_required
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
        return render(request, 'search_members.html', {'members': members,'logged_in': request.user.is_authenticated})

    return render(request, 'search_members.html', { 'logged_in': request.user.is_authenticated})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('earn')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password', 'logged_in': request.user.is_authenticated})
        else:
            return render(request, 'login.html', {'form': form, 'logged_in': request.user.is_authenticated})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'logged_in': request.user.is_authenticated})

def logout_user(request):
    logout(request)
    return redirect('login') 

def register(request):
    if request.user.is_authenticated:
        return redirect('login')
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
            return HttpResponse(template.render({'error_message': e, 'logged_in': request.user.is_authenticated}))
    template = loader.get_template('register.html')
    return HttpResponse(template.render({ 'logged_in': request.user.is_authenticated}))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Update the session to keep the user logged in after password change
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('search_members')  # Redirect to the search_members or any view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form, 'logged_in': request.user.is_authenticated})

@login_required
def increment_amount(request):
    # Get or create the Amount record for the logged-in user
    amount_record, created = Amount.objects.get_or_create(user=request.user, defaults={"amount": 0})
    
    # Increment the amount if the request is a POST
    if request.method == "POST":
        amount_record.amount += 1  # Increment by 1
        amount_record.save()
        return redirect("earn")  # Reload the page after updating

    return render(request, "increment_amount.html", {"amount": amount_record.amount, 'logged_in': request.user.is_authenticated})

@login_required
def profile_view(request):
    # Get the user's amount record
    amount_record, created = Amount.objects.get_or_create(user=request.user, defaults={"amount": 0.00})
    
    if request.method == "POST":
        # Update profile information
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        # Update user information
        user = request.user
        user.username = username
        user.email = email
        user.save()

        return redirect("profile")  # Redirect to the same page after updating

    return render(request, "profile.html", {"user": request.user, "amount": amount_record.amount, 'logged_in': request.user.is_authenticated})

@login_required
def list_members(request):
    # Query all users XSS
    members = User.objects.all()
    return render(request, 'list_members.html', {'members': members, 'logged_in': request.user.is_authenticated})

def landing_page(request):
    """
    Render the landing page for the Clicker application
    """
    context = {
        'app_name': 'Clicker',
        'tagline': 'Click Your Way to Cash!',
        'features': [
            {'title': 'Easy Clicking', 'description': 'Simple mouse clicks turn into real money'},
            {'title': 'Instant Earnings', 'description': 'Watch your balance grow with every click'},
            {'title': 'Multiple Earning Modes', 'description': 'Regular clicks, combo clicks, and bonus rounds'},
            {'title': 'Withdrawal Options', 'description': 'Multiple payment methods to cash out your earnings'}
        ],
        'how_it_works': [
            'Sign up for free',
            'Start clicking the main button',
            'Earn money for each click',
            'Cash out your earnings'
        ],
        'logged_in': request.user.is_authenticated
    }
    return render(request, 'landing.html', context)

@login_required
@csrf_exempt
def send_amount(request):
    if request.method == "POST":
        sender = request.user
        receiver_username = request.POST.get("receiver_username")
        amount_to_send = request.POST.get("amount")

        try:
            # Validate input
            if not receiver_username or not amount_to_send:
                raise ValueError("Invalid data provided.")
            amount_to_send = int(amount_to_send)
            if amount_to_send <= 0:
                raise ValueError("Amount must be greater than zero.")

            # Fetch sender and receiver Amount objects
            sender_amount, _ = Amount.objects.get_or_create(user=sender)
            receiver = User.objects.get(username=receiver_username)
            receiver_amount, _ = Amount.objects.get_or_create(user=receiver)

            # Ensure sender has sufficient balance
            if sender_amount.amount < amount_to_send:
                raise ValueError("Insufficient balance.")

            # Perform the transfer
            sender_amount.amount -= amount_to_send
            receiver_amount.amount += amount_to_send
            sender_amount.save()
            receiver_amount.save()

            return redirect("profile")  # Redirect to profile or another page after success
        except User.DoesNotExist:
            error_message = "Receiver does not exist."
        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = str(e)

        # Render the error back to the search page
        return render(request, 'search_members.html', {"error_message": error_message}) 

    return render(request, 'search_members.html')  # Redirect to the search page for non-POST requests
