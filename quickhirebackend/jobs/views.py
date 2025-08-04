from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .job_serializer import JobSerializer
from companies.models import Company
from applications.models import Application
from accounts.models import UserDetails
from subscriptions.models import CompanySubscription

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_list_create(request):
    if request.method == 'GET':
        jobs = Job.objects.select_related('company').all().order_by('-is_created')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        try:
            userDetails = UserDetails.objects.get(user_id=request.user.id)
            company = Company.objects.get(user_details=userDetails)
           
            if company.is_approved == False:
                return Response({"error": "Your company is not approved yet."}, status=status.HTTP_403_FORBIDDEN)
           
            # subscription = CompanySubscription.objects.get(company=company)
    
            # if not subscription.is_active():
            #     return Response({"error": "Your company is not subscribed."}, status=status.HTTP_403_FORBIDDEN)

        except Company.DoesNotExist:
            return Response({"error": "You need to create a company first."}, status=status.HTTP_404_NOT_FOUND)
        except CompanySubscription.DoesNotExist:
            return Response({"error": "Your company does not have a subscription."}, status=status.HTTP_403_FORBIDDEN)
        

        role = request.data.get('role')
        expected_salary = request.data.get('expected_salary')
        job_type = request.data.get('job_type')
        job_desc = request.data.get('job_desc')
        skills = request.data.get('skills')
        is_active = request.data.get('is_active')

        job = Job(company=company,role=role,expected_salary=expected_salary,job_type=job_type,job_desc=job_desc,skills=skills,is_active=is_active)
        job.save()
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # try:
        #     company = Company.objects.get(company_id=company_id)
        # except company.DoesNotExist:
        #     return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # job = Job(company=company,role=role,expected_salary=expected_salary,job_type=job_type,job_desc=job_desc,skills=skills)
        # job.save()

        # serializer = JobSerializer(job)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def available_jobs(request):
    try:
        user = UserDetails.objects.get(user_id=request.user.id)
    except UserDetails.DoesNotExist:
        user = UserDetails(user=request.user)

    applied_job_ids = Application.objects.filter(user_id=user).values_list('job_id', flat=True)

    jobs = Job.objects.filter(is_active=True).exclude(job_id__in=applied_job_ids).select_related('company').order_by('-is_created')

    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)

# search job by job name or company name

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_jobs(request):
    query = request.GET.get('query', None)
    
    try:
        user = UserDetails.objects.get(user_id=request.user.id)
    except UserDetails.DoesNotExist:
        user = UserDetails(user=request.user)
    
    # Get the list of job IDs that the user has applied to
    applied_job_ids = Application.objects.filter(user_id=user).values_list('job_id', flat=True)
    
    # Filter jobs that are active and have not been applied to by the user
    jobs = Job.objects.filter(is_active=True).exclude(job_id__in=applied_job_ids)
    
    # Apply the search filter if a query is provided
    if query:
        jobs = jobs.filter(role__icontains=query)
    
    # Select related company information and order the jobs by creation date
    jobs = jobs.select_related('company').order_by('-is_created')
    
    # Serialize the data
    serializer = JobSerializer(jobs, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = JobSerializer(job, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# employer part

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employer_jobs(request):
    user = UserDetails.objects.get(user_id=request.user.id)

    if user.user_type != 'Employer':
        return Response({"error": "You are not authorized to view this."}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        company = Company.objects.get(user_details=user)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
    
    is_active_status = request.query_params.get('is_active', None)

    if is_active_status is not None:
        is_active_status = is_active_status.lower() == 'true'
        jobs = Job.objects.filter(company=company, is_active=is_active_status).order_by('-is_created')
    else:
        jobs = Job.objects.filter(company=company).order_by('-is_created')
    
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

# get the count for the active and inactive jobs

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_status_count(request):
    user = UserDetails.objects.get(user_id=request.user.id)

    company = Company.objects.get(user_details=user)

    active_count = Job.objects.filter(company=company,is_active=True).count()
    inactive_count = Job.objects.filter(company=company,is_active=False).count()

    return Response({
        "active_jobs": active_count,
        "inactive_jobs": inactive_count
    })