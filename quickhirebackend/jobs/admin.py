from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Job._meta.fields]

admin.site.register(Job, JobAdmin)

# Register your models here.
