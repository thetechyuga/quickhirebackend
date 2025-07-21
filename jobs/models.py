from django.db import models
from companies.models import Company
class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    expected_salary = models.CharField(max_length=200, default="Not disclosed") # String of range - 20L to 50L OR unspecifiec
    job_type = models.CharField(max_length=200 ) # part time, full time, Remote
    job_desc = models.TextField()
    skills = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role