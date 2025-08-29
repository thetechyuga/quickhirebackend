from django.db import models

class UserDetails(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_photo = models.ImageField(upload_to='profile_photos/', default="profile_photos/default/profile_image_placeholder.png")
    #new added
    resumeFile = models.FileField(upload_to="resumes/", null=True, blank=True)
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
            # ✅ Delete old photo if replaced (not default)
            this = UserDetails.objects.get(user_id=self.user_id)
            if not "default" in this.user_photo.name and this.user_photo != self.user_photo:
                this.user_photo.delete(save=False)
            # ✅ Delete old resume if replaced
            if this.resumeFile and this.resumeFile != self.resumeFile:
                this.resumeFile.delete(save=False)
        except UserDetails.DoesNotExist:
            pass

        super(UserDetails, self).save(*args, **kwargs)

class EducationJourney(models.Model):
    userdetails = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='education_journeys')
    educationJourneyId = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    university = models.CharField(max_length=255)
    startYear = models.IntegerField()
    passingYear = models.IntegerField()
    grade = models.CharField(max_length=50, null=True, blank=True)   # <-- changed from DecimalField
    course_type = models.CharField(max_length=255)  # full time / distance / online
    #resumeUrl = models.FileField(upload_to="resumes/", null=True, blank=True)
    skills = models.JSONField(default=list, blank=True)      # stores list of skills
    languages = models.JSONField(default=list, blank=True)  # stores list of languages

    def __str__(self):
        return f"{self.course} at {self.university}"


class ExperienceJourney(models.Model):
    UserDetails = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='experience_journeys')
    ExperienceJourneyId = models.AutoField(primary_key=True)

    # Work Experience Fields
    totalExperience = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    companyName = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    skills = models.CharField(max_length=255, null=True, blank=True)
    startYear = models.IntegerField()
    endYear = models.IntegerField()

    # Education-like Fields
    highestQualification = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    courseType = models.CharField(max_length=255, null=True, blank=True)  # full time or distance or online
    specialization = models.CharField(max_length=255, null=True, blank=True)
    universityName = models.CharField(max_length=255, null=True, blank=True)

    # Resume Upload
    resumeFile = models.FileField(upload_to="resumes/", null=True, blank=True)

    def __str__(self):
        return f"{self.designation} at {self.company_name}"

