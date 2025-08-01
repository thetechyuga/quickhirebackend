from django.db import models
from accounts.models import UserDetails
from companies.models import Company
class Payment(models.Model):
    payment_id = models.CharField(max_length=255)  
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='payments')
    datetime = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Payment {self.payment_id} for User {self.user.name}"

class CompanyPayment(models.Model):
    payment_id = models.CharField(max_length=255)  
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_payments')
    datetime = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Payment {self.payment_id} for User {self.company.company_name}"