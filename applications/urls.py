from django.urls import path
from . import views

urlpatterns = [
    path('applications/', views.application_list_create, name='application-list-create'),
    path('applications/<int:pk>/', views.application_detail, name='application-detail'),
    path('applications/users/<int:user_id>/', views.application_list_by_user, name='application-list-by-user'),
    path('applications/users/<int:user_id>/status/<str:status_filter>/', views.search_applications_by_user_and_status, name='search_applications_by_user_and_status'),
    path('applications/jobs/<int:job_id>/', views.application_list_by_job, name='application-list-by-job'),
    path('applications/last7days/', views.applications_last_7_days, name='applications_last_7_days'),
]
