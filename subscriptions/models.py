# models.py
from django.db import models
from django.utils import timezone
from accounts.models import UserDetails
from datetime import datetime
from companies.models import Company

class Subscription(models.Model):
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE, related_name='user_subscription')
    payment_id = models.CharField(max_length=300,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):

        if isinstance(self.start_date, str):
            self.start_date = datetime.fromisoformat(self.start_date)
        if isinstance(self.end_date, str):
            self.end_date = datetime.fromisoformat(self.end_date)

        return self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.name} - {'Active' if self.is_active() else 'Inactive'}"
    
class CompanySubscription(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='company_subscription')
    payment_id = models.CharField(max_length=300,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):

        if isinstance(self.start_date, str):
            self.start_date = datetime.fromisoformat(self.start_date)
        if isinstance(self.end_date, str):
            self.end_date = datetime.fromisoformat(self.end_date)

        return self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.name} - {'Active' if self.is_active() else 'Inactive'}"
    

class SubscriptionPlans(models.Model):
    PLAN_CHOICES = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]
    
    subscription_name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=PLAN_CHOICES)

    def __str__(self):
        return f"{self.subscription_name} ({self.type}) - ${self.price}"

class CompanySubscriptionPlans(models.Model):
    PLAN_CHOICES = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
        ('OneTime', 'OneTime'),
    ]
    
    subscription_name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=PLAN_CHOICES)

    def __str__(self):
        return f"{self.subscription_name} ({self.type}) - ${self.price}"
