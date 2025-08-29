# urls.py
from django.urls import path
from .views import upload_resume, user_list_create,user_detail, education_journey_detail, education_journey_list_create,education_journey_for_user, experience_journey_detail, experience_journey_for_user, experience_journey_list_create, upload_profile_picture, get_image_url
from .account_deletion_views import delete_user_data, verify_otp_view, account_deleted
from django.conf import settings
from django.conf.urls.static import static
from . import views as user_Views


urlpatterns = [
    path('users/', user_list_create, name='user-list-create'),
    path('get-image-url/', get_image_url, name='get-image-url'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('educationjourneys/', education_journey_list_create, name='educationjourney-list-create'),
    path('educationjourneys/<int:pk>/', education_journey_detail, name='educationjourney-detail'),
    path('educationjourneys/users/<int:user_id>/', education_journey_for_user, name='educationjourney-for-user'),
    path('experiencejourneys/', experience_journey_list_create, name='experiencejourney-list-create'),
    path('experiencejourneys/<int:pk>/', experience_journey_detail, name='experiencejourney-detail'),
    path('experiencejourneys/users/<int:user_id>/', experience_journey_for_user, name='experiencejourney-for-user'),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('delete_user_data/', delete_user_data, name='delete_user_data'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('account-deleted/', account_deleted, name='account_deleted'),
    path('user-login/', user_Views.login_user , name='login_user'),
    path('verify-login/', user_Views.verify_otp_view , name='verify_login'),
    path("upload_resume/", upload_resume, name="upload_resume"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
