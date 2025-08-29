from rest_framework import serializers
from .models import UserDetails, EducationJourney

class EducationJourneySerializer(serializers.ModelSerializer):
    userdetails = serializers.PrimaryKeyRelatedField(queryset=UserDetails.objects.all())

    class Meta:
        model = EducationJourney
        fields = '__all__'
