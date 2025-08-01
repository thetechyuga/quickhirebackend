import random
import string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .forms import UsernameForm, OtpForm
from accounts.models import UserDetails

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def delete_user_data(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)

                # Generate and send OTP
                otp = generate_otp()
                request.session['otp'] = otp  # Store OTP in session
                request.session['username'] = username  # Store OTP in session
                send_otp_email(user.email, otp)  # Send OTP to the user's email
                return redirect('verify_otp')
            except User.DoesNotExist:
                return JsonResponse({'message': 'Username does not exist!'}, status=400)
    else:
        form = UsernameForm()
    return render(request, 'accounts/username.html', {'form': form})

def verify_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            session_otp = request.session.get('otp')
            username = request.session.get('username')

            if otp == session_otp:
                try:
                    user = User.objects.get(username=username)
                    userDetails = UserDetails.objects.get(email=user.email)
                    user.delete() 
                    userDetails.delete()
                    del request.session['otp']  # Clear OTP from session
                    return redirect('account_deleted')
                except User.DoesNotExist:
                    return JsonResponse({'message': 'User not found!'}, status=400)
            else:
                return JsonResponse({'message': 'Invalid OTP!'}, status=400)
    else:
        form = OtpForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})


def account_deleted(request):
    return render(request, 'accounts/account_deleted.html')