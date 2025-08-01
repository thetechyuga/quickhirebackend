from django.db import models

class UserDetails(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_photo = models.ImageField(upload_to='profile_photos/', default="profile_photos/default/profile_image_placeholder.png")
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    role = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    user_type = models.CharField(max_length=20, default="Seeker"); # either Employer or Seeker
    languages = models.CharField(max_length=500, blank=True, null=True)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=6 , default="888888")

    def __str__(self):
        return f"{self.name} has id: {self.user_id}"

    def save(self, *args, **kwargs):
        try:
            this = UserDetails.objects.get(user_id=self.user_id)
            if not "default" in this.user_photo.name and this.user_photo != self.user_photo:
                this.user_photo.delete(save=False)
        except UserDetails.DoesNotExist:
            pass

        super(UserDetails, self).save(*args, **kwargs)

class EducationJourney(models.Model):
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='education_journeys')
    education_journey_id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=255)
    institute_name = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    course_type = models.CharField(max_length=255) # full time or distance or online

    def __str__(self):
        return f"{self.course} at {self.institute_name}"

class ExperienceJourney(models.Model):
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='experience_journeys')
    experience_journey_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    experience_type = models.CharField(max_length=255) # full time or distance or online

    def __str__(self):
        return f"{self.role} at {self.company_name}"
