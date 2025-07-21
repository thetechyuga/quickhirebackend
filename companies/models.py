from django.db import models
from accounts.models import UserDetails

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='employer_details')
    company_name = models.CharField(max_length=200)
    company_title = models.CharField(max_length=200, default='Empowering Growth')
    company_desc = models.CharField(max_length=400, default='',blank=True)
    founded_year = models.CharField(max_length=4, default='',blank=True)
    company_link = models.URLField(max_length=200, default='',blank=True)
    linkedin_link = models.URLField(max_length=200, default='',blank=True)
    industry = models.CharField(max_length=200, default='',blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', default="profile_photos/default/profile_image_placeholder.png")
    company_background = models.ImageField(upload_to='company_background/', default="company_background/default.jpg")
    location = models.CharField(max_length=200 ,blank=True)
    is_approved = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField (auto_now=True)

    def __str__(self):
        return f"{self.company_name} has {self.company_id}"

    def save(self, *args, **kwargs):
        try:
            this = Company.objects.get(company_id=self.company_id)
            if not "default" in this.company_logo.name and this.company_logo != self.company_logo:
                this.company_logo.delete(save=False)
        except Company.DoesNotExist:
            pass  

        try:
            this = Company.objects.get(company_id=self.company_id)
            if not "default" in this.company_background.name and this.company_background != self.company_background:
                this.company_background.delete(save=False)
        except Company.DoesNotExist:
            pass  

        super(Company, self).save(*args, **kwargs)