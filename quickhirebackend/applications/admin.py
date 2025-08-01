from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Application._meta.fields]


admin.site.register(Application, ApplicationAdmin)
