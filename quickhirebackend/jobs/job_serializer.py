from rest_framework import serializers
from .models import Job
from companies.company_serializer import CompanySerializer

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Job
        fields = '__all__'
