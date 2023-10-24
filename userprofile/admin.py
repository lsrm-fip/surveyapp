from django.contrib import admin
from .models import FacultyList, MajorList, ProfileList

admin.site.register(FacultyList)
admin.site.register(MajorList)
admin.site.register(ProfileList)