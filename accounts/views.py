# accounts/views.py
# Handles user authentication: registration, login, logout

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    """
    Handles user registration.
    GET: Displays registration form.
    POST: Creates new user account.
    """
    
    # Check if form was submitted
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        
        # Create new user in database
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Log the user in automatically after registration
        login(request, user)
        
        # Show welcome message
        messages.success(request, f'Account created successfully! Welcome {first_name}.')
        
        # Redirect to dashboard
        return redirect('dashboard')
    
    # GET request - display registration form
    return render(request, 'accounts/register.html')


def user_login(request):
    """
    Handles user login.
    GET: Displays login form.
    POST: Authenticates user and logs them in.
    """
    
    # Check if form was submitted
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user (checks username and password against database)
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication succeeded
        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    # GET request - display login form
    return render(request, 'accounts/login.html')


def user_logout(request):
    """
    Logs out the current user.
    """
    # Log the user out
    logout(request)
    
    # Show message
    messages.success(request, 'You have been logged out.')
    
    # Redirect to login page
    return redirect('home')