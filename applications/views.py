from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Application
from .application_serializer import ApplicationSerializer
from jobs.models import Job
from accounts.models import UserDetails

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDay
from companies.models import Company

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def application_list_create(request):
    if request.method == 'GET':
        applications = Application.objects.select_related('user_id').all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        user_id = request.data.get('user_id')
        job_id = request.data.get('job_id')
        applicationStatus = request.data.get('status')

        try:
            job = Job.objects.get(job_id=job_id)
        except job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = UserDetails.objects.get(user_id=user_id)
        except UserDetails.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        application = Application(user_id=user, job=job, status=applicationStatus)
        application.save()
        
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def application_detail(request, pk):
    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# search applications by user

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def application_list_by_user(request, user_id):
    if request.method == 'GET':
        applications = Application.objects.filter(user_id=user_id)
        if applications.exists():
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No applications found for this user'}, status=status.HTTP_404_NOT_FOUND)


# application by status and userId

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_applications_by_user_and_status(request, user_id, status_filter):
    try:
        # Filter applications based on user_id and status
        applications = Application.objects.filter(user_id=user_id, status=status_filter).select_related('job')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#  applications by job

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def application_list_by_job(request, job_id):
    if request.method == 'GET':
        job = get_object_or_404(Job, pk=job_id)
        status_filter = request.query_params.get('status', None)

        if status_filter:
            applications = Application.objects.filter(job=job,status=status_filter).order_by('-is_created')
        else:
            applications = Application.objects.filter(job=job).order_by('-is_created')
            
        if applications.exists():
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No applications found for this job'}, status=status.HTTP_404_NOT_FOUND)
        
#  applications data for last 7 days for plotting graph!

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def applications_last_7_days(request):
    
    userDetails = UserDetails.objects.get(user_id=request.user.id)

    company = Company.objects.get(user_details=userDetails)
    
    # Get all jobs posted by this company
    jobs = Job.objects.filter(company=company)
    
    # Calculate the date range for the last 7 days
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)
    
    # Get the applications for the last 7 days and group by day using the `is_created` field
    applications = Application.objects.filter(
        job__in=jobs,
        is_created__range=[start_date, end_date]
    ).annotate(
        day=TruncDay('is_created')
    ).values('day').annotate(
        count=Count('application_id')
    ).order_by('day')

    applications_data = {
        (start_date + timedelta(days=i)).strftime('%d/%m'): 0 for i in range(7)
    }
    
    # Update the dictionary with the actual counts from the database
    for app in applications:
        formatted_date = app['day'].strftime('%d/%m')
        applications_data[formatted_date] = app['count']
    
    # Format the data as a list of dictionaries with date formatted as "day/month"
    response_data = [
        {'date': date, 'applications_count': count}
        for date, count in applications_data.items()
    ]
    
    return Response(
        response_data,
        status=status.HTTP_200_OK
    )