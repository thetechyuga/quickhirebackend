from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from .models import ExperienceJourney
from .experience_serializer import ExperienceJourneySerializer

from .models import EducationJourney
from .education_serializer import EducationJourneySerializer

from .user_details_serializer import UserDetailSerializer
from .models import UserDetails

import os
from django.conf import settings

import json
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.contrib.auth.models import User

# user Views

@api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
def user_list_create(request):
    if request.method == 'GET':
        users = UserDetails.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = UserDetails.objects.get(pk=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_data = UserDetailSerializer(user).data
        if not user_data.get('user_photo'):
            user_data['user_photo'] = "/media/profile_photos/default/profile_image_placeholder.png"
        return Response(user_data)

    elif request.method == 'PUT':
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = UserDetailSerializer(user, data=request.data, partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Education Journey Views

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def education_journey_list_create(request):
    if request.method == 'GET':
        education_journeys = EducationJourney.objects.all()
        serializer = EducationJourneySerializer(education_journeys, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EducationJourneySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def education_journey_detail(request, pk):
    try:
        education_journey = EducationJourney.objects.get(pk=pk)
    except EducationJourney.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EducationJourneySerializer(education_journey)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = EducationJourneySerializer(education_journey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = EducationJourneySerializer(education_journey, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        education_journey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# get the joruney of user by their id

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def education_journey_for_user(request, user_id):
    education_journeys = EducationJourney.objects.filter(user_details=user_id)

    if not education_journeys.exists():
        return Response({'error': 'No education journeys found for this user'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EducationJourneySerializer(education_journeys, many=True)
    return Response(serializer.data)


# Experience Journey Views

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def experience_journey_list_create(request):
    if request.method == 'GET':
        experience_journeys = ExperienceJourney.objects.all()
        serializer = ExperienceJourneySerializer(experience_journeys, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExperienceJourneySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def experience_journey_detail(request, pk):
    try:
        experience_journey = ExperienceJourney.objects.get(pk=pk)
    except ExperienceJourney.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExperienceJourneySerializer(experience_journey)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ExperienceJourneySerializer(experience_journey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = ExperienceJourneySerializer(experience_journey, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        experience_journey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# get the joruney of user by their id

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def experience_journey_for_user(request, user_id):
    experience_journeys = ExperienceJourney.objects.filter(user_details=user_id)

    if not experience_journeys.exists():
        return Response({'error': 'No experience journeys found for this user'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ExperienceJourneySerializer(experience_journeys, many=True)
    return Response(serializer.data)

# user photo APIs

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request):
    if request.method == 'GET':
        try:
            user_profile = UserDetails.objects.get(user_id=request.user.id)
            serializer = UserDetailSerializer(user_profile)
            return Response(serializer.data)
        except UserDetails.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try:
            user_profile = UserDetails.objects.get(user_id=request.user.id)
        except UserDetails.DoesNotExist:
            user_profile = UserDetails(user=request.user)

        # Update with the new user_photo
        if 'user_photo' in request.FILES:
            user_profile.user_photo = request.FILES['user_photo']

        user_profile.save()

        serializer = UserDetailSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_image_url(request):
    image_data = {
        "image_url": settings.MEDIA_URL + "1000029253.png"
    }
    return JsonResponse(image_data)

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

@api_view(['POST'])
def login_user(request):
    try :
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try :
            users = get_object_or_404(UserDetails, email = email)
        except:
            return Response({'error': 'User Not Found'} ,status=status.HTTP_400_BAD_REQUEST)

        if users is None:
            return Response({'error': 'User Not Found With The Email.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = get_random_string(length=6, allowed_chars='1234567890')
        users.otp = otp
        users.save()

        send_otp_email(users.email, otp)
        return Response({'message' : 'Otp Sent Success fully'} ,status=status.HTTP_200_OK)

    except Exception as e :
        return Response({'error': str(e)} ,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_otp_view(request):
    data = json.loads(request.body)
    otp = data.get('otp')
    email = data.get('email')
    usersDetails = get_object_or_404(UserDetails, email = email)
    user = get_object_or_404(User, username = usersDetails.name)
    sent_otp = usersDetails.otp

    if otp == sent_otp:
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserDetailSerializer(instance=usersDetails)
        return Response({"token":token.key, "user":serializer.data})
        # return JsonResponse({'message': 'User Verified !!'}, status=status.HTTP_200_OK )
    else:
        return JsonResponse({'message': 'Invalid OTP!'}, status=status.HTTP_400_BAD_REQUEST )

