from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Subscription, CompanySubscription, SubscriptionPlans, CompanySubscriptionPlans
from .subs_serializers import SubscriptionSerializer, CompanySubscriptionSerializer, SubscriptionPlansSerializer, CompanySubscriptionPlansSerializer
from accounts.models import UserDetails
from companies.models import Company
from payments.models import Payment, CompanyPayment
from django.utils import timezone

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    if request.method == 'GET':
        try:
            user = request.user.id
            userDetails = UserDetails.objects.get(user_id=user)
            subscription = Subscription.objects.get(user=userDetails)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response({'is_active': False})
    
    elif request.method == 'POST':
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            payment_id = request.data.get('payment_id')
           
            try:
                user = UserDetails.objects.get(user_id=request.user.id)
            except user.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


            # Update the subscription details
            subscription, created = Subscription.objects.update_or_create(
                user=user,
                 defaults={
                'start_date': start_date,
                'end_date': end_date,
                'payment_id': payment_id,
                }
            )

            Payment.objects.create(
                user=user,
                    payment_id= payment_id,
                    datetime= timezone.now(),  # Set datetime to now
            )

            # Serialize and return the updated subscription data
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_subscription_status(request):
    if request.method == 'GET':
        try:
            user = UserDetails.objects.get(user_id=request.user.id)
            
            company = Company.objects.get(user_details=user)

            subscription = CompanySubscription.objects.get(company=company)
            serializer = CompanySubscriptionSerializer(subscription)
            return Response(serializer.data)
        except CompanySubscription.DoesNotExist:
            return Response({'is_active': False})
    
    elif request.method == 'POST':
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            payment_id = request.data.get('payment_id')

            try:
                company = Company.objects.get(user_details = request.user.id)
            except Company.DoesNotExist:
                return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

            subscription, created = CompanySubscription.objects.update_or_create(
                company=company,
                 defaults={
                'start_date': start_date,
                'end_date': end_date,
                'payment_id': payment_id,
                }
            )

            CompanyPayment.objects.create(
                company=company,
                    payment_id= payment_id,
                    datetime= timezone.now(),  # Set datetime to now
            )

            serializer = CompanySubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_subscription(request, company_id):
    try:
        company = Company.objects.get(company_id=company_id)
        subscription = CompanySubscription.objects.get(company=company)
        subscription.delete()
        return Response({'message': 'Deleted Succesfully'},status=status.HTTP_204_NO_CONTENT)
    except CompanySubscription.DoesNotExist:
        return Response({"message": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscription_plans(request):
    if request.method == 'GET':
        subscription_plans = SubscriptionPlans.objects.all().order_by('price')
        serializer = SubscriptionPlansSerializer(subscription_plans, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def company_subscription_plans(request):
    if request.method == 'GET':
        subscription_plans = CompanySubscriptionPlans.objects.all().order_by('price')
        serializer = CompanySubscriptionPlansSerializer(subscription_plans, many=True)
        return Response(serializer.data)