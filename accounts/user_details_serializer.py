from rest_framework import serializers
from .models import UserDetails

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'