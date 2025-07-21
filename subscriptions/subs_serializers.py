# serializers.py
from rest_framework import serializers
from .models import Subscription, CompanySubscription, SubscriptionPlans, CompanySubscriptionPlans

class SubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['user', 'start_date', 'end_date', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active()

class CompanySubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = CompanySubscription
        fields = ['company', 'start_date', 'end_date', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active()

class SubscriptionPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlans
        fields = '__all__'

class CompanySubscriptionPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySubscriptionPlans
        fields = '__all__'
