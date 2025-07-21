from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import company_list_create, company_detail, company_detail_by_id, upload_company_profile_image,upload_company_banner

urlpatterns = [
    path('companies/', company_list_create, name='company-list-create'),
    path('company-detail/', company_detail, name='company_detail'),
    path('company-detail-by-id/<int:pk>/', company_detail_by_id, name='company_detail_by_id'),
    path('update-company-logo/', upload_company_profile_image, name='upload_company_profile_image'),
    path('update-company-banner/', upload_company_banner, name='upload_company_banner'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
