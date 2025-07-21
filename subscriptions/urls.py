# urls.py
from django.urls import path
from .views import subscription_status, company_subscription_status,delete_subscription, subscription_plans, company_subscription_plans

urlpatterns = [
    path('subscription-plans/', subscription_plans, name='subscription-plans'),
    path('company-subscription-plans/', company_subscription_plans, name='company-subscription-plans'),
    path('subscription-status/', subscription_status, name='subscription-status'),
    path('company-subscription-status/', company_subscription_status, name='company_subscription_status'),
    path('delete-company-subscription-status/<int:company_id>/', delete_subscription, name='delete_subscription'),
]
