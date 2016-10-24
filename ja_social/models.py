from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse_lazy


import datetime

MAX_CHAR_LENGTH = 50

COUNTY_OPTIONS = (
    ("Alamance", "Alamance"),
    ("Forsyth", "Forsyth"),
    ("Guilford", "Guilford"),
    ("Montgomery", "Montgomery"),
    ("Randolph", "Randolph"),
    ("Rockingham", "Rockingham"),
    ("Other", "Other")
)

JA_PROGRAM_OPTIONS = (
    ("JA Ourselves", "JA Ourselves"),
    ("JA Our Families", "JA Our Families"),
    ("JA Our Community", "JA Our Community"),
    ("JA Our City", "JA Our City"),
    ("JA Our Region", "JA Our Region"),
    ("JA Our Nation", "JA Our Nation"),
    ("JA Economics for Success", "JA Economics for Success"),
    ("JA Global Marketplace - Kit Based", "JA Global Marketplace - Kit Based"),
    ("JA Global Marketplace - Blended Model", "JA Global Marketplace - Blended Model"),
    ("JA It's My Future", "JA It's My Future"),
    ("JA Be Entrepreneurial", "JA Be Entrepreneurial"),
    ("JA Career", "JA Career"),
    ("JA Company Program - Blended Model", "JA Company Program - Blended Model"),
    ("JA Economics", "JA Economics"),
    ("JA Exploring Economics", "JA Exploring Economics"),
    ("JA Job Shadow", "JA Job Shadow"),
    ("JA Personal Financial", "JA Personal Financial"),
    ("JA Personal Financial - Blended Model", "JA Personal Financial - Blended Model"),
    ("JA Titan", "JA Titan")

)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    company = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="uploads/profile_pics/", null=True, default=None)
    activation_key = models.CharField(max_length=40, default="")
    key_expires = models.DateTimeField(default=datetime.date.today)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse_lazy('ja_social:user_view', kwargs={'pk': self.pk})


class VolunteerRecord(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    county = models.CharField(max_length=MAX_CHAR_LENGTH, choices=COUNTY_OPTIONS)
    school_name = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False, null=False)
    JA_program = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False, null=False, default="", choices=JA_PROGRAM_OPTIONS)
    hours = models.PositiveIntegerField(blank=False, null=False, default=0)
    date = models.DateField(blank=False, null=False, default=datetime.date.today)
    verified = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return "%s: %s %s (%d)" % (self.user_profile.user.get_full_name(), self.school_name, self.JA_program, self.hours)


class PhotoRecord(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="uploads/gallery_pictures/", blank=False, null=False)
    date_uploaded = models.DateField(default=datetime.date.today, null=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)



