from django.contrib import admin
from .models import Subscription, CompanySubscription, SubscriptionPlans, CompanySubscriptionPlans

admin.site.register(Subscription)
admin.site.register(CompanySubscription)

@admin.register(SubscriptionPlans)
class SubscriptionPlansAdmin(admin.ModelAdmin):
    list_display = ('subscription_name', 'price', 'type')
    search_fields = ('subscription_name', 'type')

@admin.register(CompanySubscriptionPlans)
class CompanySubscriptionPlansAdmin(admin.ModelAdmin):
    list_display = ('subscription_name', 'price', 'type')
    search_fields = ('subscription_name', 'type')

