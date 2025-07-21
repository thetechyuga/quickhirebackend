from django import forms

class UsernameForm(forms.Form):
    username = forms.CharField(label='Enter your username', max_length=150)

class OtpForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6)
