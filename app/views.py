from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')


def logout(request):
    return render(request, 'landing.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            
            return redirect('user_dashboard')  # Redirect to the user dashboard
        else:
            messages.error(request, "Invalid credentials, please try again.")
    
    return render(request, 'signin.html')

import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser
import re
import os

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        profile_image = request.FILES.get('profile_image')

        # Minimal registration logic (without validation)
        password = generate_random_password()
        hashed_password = make_password(password)

        user = CustomUser.objects.create(
            username=username,
            email=email,
            phone=phone,
            address=address,
            password=hashed_password,
            profile_image=profile_image
        )

        subject = "Welcome to Bank Coaching Centre"
        message = f"""
Hi {username},

Your registration was successful.

Here are your login credentials:

Username: {username}
Password: {password}

Login here: http://yourdomain.com/signin/

Please change your password after logging in.

Regards,
Bank Coaching Centre
"""
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        messages.success(request, "Registration successful! Check your email for login credentials.")
        return redirect('signin')

    return render(request, 'signup.html')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .models import CustomUser

@csrf_exempt
def ajax_validate_field(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value').strip()
        error = ""

        if field == "username":
            if not value:
                error = "Username is required."
            elif CustomUser.objects.filter(username=value).exists():
                error = "Username already exists."

        elif field == "email":
            if not value.endswith(".com"):
                error = "Email must end with .com."
            elif CustomUser.objects.filter(email=value).exists():
                error = "Email already exists."

        elif field == "phone":
            if not re.fullmatch(r"\d{10}", value):
                error = "Enter a valid 10-digit phone number."
            elif CustomUser.objects.filter(phone=value).exists():
                error = "Phone number already exists."

        elif field == "address":
            if len(value) < 10:
                error = "Address must be at least 10 characters long."

        return JsonResponse({"error": error})

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def user_dashboard(request):
    user = request.user  # Current logged-in user

    if request.method == 'POST':
        # Update the user profile if there's a POST request (e.g., updating the address or phone)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, 'user_landing.html', {'user': user})




