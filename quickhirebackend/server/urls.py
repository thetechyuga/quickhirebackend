from django.urls import re_path, path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login/$', views.login),
    re_path('signup/', views.signup),
    re_path('verify-signup-otp/', views.verify_signup_otp),
    re_path('logout/', views.logout),
    re_path('test_token', views.test_token),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('',include('accounts.urls')),
    path('',include('jobs.urls')),
    path('',include('companies.urls')),
    path('',include('applications.urls')),
    path('',include('user_messages.urls')),
    path('',include('subscriptions.urls')),
]
