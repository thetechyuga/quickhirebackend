from django.contrib import admin

from .models import Payment, CompanyPayment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'datetime')
    search_fields = ('payment_id', 'user__user_id')

@admin.register(CompanyPayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'company', 'datetime')
    search_fields = ('payment_id', 'company__company_id')