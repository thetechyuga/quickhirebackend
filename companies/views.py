from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .company_serializer import CompanySerializer
from accounts.models import UserDetails
import os
from django.conf import settings

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_list_create(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        userDetails = UserDetails.objects.get(user_id=request.user.id)

        if userDetails.user_type != 'Employer':
            return Response({"error": "Only employers can create a company."}, status=status.HTTP_403_FORBIDDEN)
        
        company_name = request.data.get('company_name')
        location = request.data.get('location')
        company_title = request.data.get('company_title', "Empowering Growth")
        company_desc = request.data.get('company_desc',"")
        company_link = request.data.get('company_link',"")
        linkedin_link = request.data.get('linkedin_link',"")
        industry = request.data.get('industry',"")
        founded_year = request.data.get('founded_year',"")


        company = Company(user_details=userDetails,company_name=company_name,location=location,company_title=company_title,company_desc=company_desc,company_link=company_link,linkedin_link=linkedin_link,industry=industry,founded_year=founded_year)
        company.save()
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_detail(request):

    userDetails = UserDetails.objects.get(user_id=request.user.id)

    try:
        company = Company.objects.get(user_details=userDetails)
    except Company.DoesNotExist:
        return Response('Company not found for the user',status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        company_data = CompanySerializer(company).data
        if not company_data.get('company_logo'):
            company_data['company_logo'] = "media/profile_photos/default/profile_image_placeholder.png"
        return Response(company_data)

    elif request.method == 'PATCH':
        serializer = CompanySerializer(company, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_detail_by_id(request, pk):

    try:
        company = Company.objects.get(company_id=pk)
    except Company.DoesNotExist:
        return Response('Company not found for the user',status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    
# upload image apis

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_company_profile_image(request):
    if request.method == 'GET':
        try:
            company = Company.objects.get(user=request.user)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        user = UserDetails.objects.get(user_id=request.user.id)
        try:
            company = Company.objects.get(user_details=user)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update with the new company_logo
        if 'company_logo' in request.FILES:
            company.company_logo = request.FILES['company_logo']
            company.save()
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_company_banner(request):
    if request.method == 'GET':
        try:
            company = Company.objects.get(user=request.user)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        user = UserDetails.objects.get(user_id=request.user.id)
        try:
            company = Company.objects.get(user_details=user)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the older company_background if it exists
        if company.company_background and company.company_background.name != 'company_background/default.jpg':
            old_image_path = os.path.join(settings.MEDIA_ROOT, company.company_background.name)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # Update with the new company_background
        if 'company_background' in request.FILES:
            company.company_background = request.FILES['company_background']
            company.save()
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)