from django.contrib import admin
from .models import UserProfile, VolunteerRecord, PhotoRecord

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(VolunteerRecord)
admin.site.register(PhotoRecord)
