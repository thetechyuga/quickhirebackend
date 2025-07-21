from django.db import models
from accounts.models import UserDetails
from jobs.models import Job


class Application(models.Model):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='application_user_id')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='application_job')
    application_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_id} was applied by {self.user_id.name} on Company Id {self.job.company.company_id}"
