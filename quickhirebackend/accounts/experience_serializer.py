from rest_framework import serializers
from .models import UserDetails, ExperienceJourney

class ExperienceJourneySerializer(serializers.ModelSerializer):
    userdetails = serializers.PrimaryKeyRelatedField(queryset=UserDetails.objects.all())

    class Meta:
        model = ExperienceJourney
        fields = '__all__'
