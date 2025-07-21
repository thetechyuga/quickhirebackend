# urls.py
from django.urls import path
from .views import job_list_create, job_detail, available_jobs, get_employer_jobs,job_status_count, search_jobs

urlpatterns = [
    path('jobs/', job_list_create, name='job_list_create'),
    path('jobs/<int:pk>/', job_detail, name='job_detail'),
    path('available-jobs/', available_jobs, name='available-jobs'),
    path('search-jobs/', search_jobs, name='search-jobs'),
    path('get-employer-jobs/', get_employer_jobs, name='get_employer_jobs'),
    path('job-status-count/', job_status_count, name='job_status_count'),
]