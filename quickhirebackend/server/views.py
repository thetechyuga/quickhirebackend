from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.user_details_serializer import UserDetailSerializer
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserDetails
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data= request.data)

#     if serializer.is_valid():
#         email = serializer.validated_data.get('email')
#         if User.objects.filter(email=email).exists():
#             return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         # insert the user into userDetails table as well
#         user_details = UserDetails.objects.create(
#             user_id=user.id,
#             name = user.username,
#             email=user.email
#         )

#         return Response({"token":token.key, "user":serializer.data})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username= request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Incorrect password! kindly check and try again"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key, "user":serializer.data})

    return Response({})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed! for {}".format(request.user.email))


# privacy policy

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms(request):
    return render(request, 'terms_and_conditions.html')

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

#new api for signup verify otp and login
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Save User
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()

        # Generate OTP
        otp = get_random_string(length=6, allowed_chars="1234567890")

        # Create UserDetails
        user_details = UserDetails.objects.create(
            user_id=user.id,
            name=user.username,
            email=user.email,
            otp=otp
        )

        # Send OTP via email
        send_otp_email(user.email, otp)

        return Response({"message": "Signup successful, please verify OTP sent to your email."}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_signup_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_details = UserDetails.objects.get(email=email)
    except UserDetails.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if user_details.otp != otp:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch User model
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Auth User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Generate token
    token, created = Token.objects.get_or_create(user=user)

    # Serialize user details
    serializer = UserDetailSerializer(user_details)

    return Response({
        "token": token.key,
        "user": serializer.data
    }, status=status.HTTP_200_OK)