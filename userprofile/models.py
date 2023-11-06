from django.db import models
from authentication.models import User


class FacultyList(models.Model):
    class Meta:
        verbose_name_plural = "Faculties"

    faculty = models.CharField(max_length=255)

    def __str__(self):
        return self.faculty


class MajorList(models.Model):
    faculty = models.ForeignKey(FacultyList, on_delete=models.CASCADE)
    major = models.CharField(max_length=255)

    def __str__(self):
        return self.major


class ProfileList(models.Model):
    GENDER = [
        ("L", "Laki-Laki"),
        ("P", "Perempuan"),
    ]

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=255, blank=False, null=True)
    nim = models.CharField(max_length=22, blank=False, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=False, default='L')    
    faculty = models.ForeignKey(FacultyList, on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(MajorList, on_delete=models.SET_NULL, null=True)
    batch = models.CharField(max_length=4, null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        return self.fullname
