from rest_framework import serializers
from .models import Application
from accounts.models import UserDetails
from jobs.models import Job
from jobs.job_serializer import JobSerializer
from accounts.user_details_serializer import UserDetailSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job = JobSerializer(read_only=True)
    user_id = UserDetailSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
