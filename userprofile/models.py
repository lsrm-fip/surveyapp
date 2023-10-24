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

    BATCH = [
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
    ]

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=False, default='L')
    faculty = models.ForeignKey(FacultyList, on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(MajorList, on_delete=models.SET_NULL, null=True)
    batch = models.CharField(max_length=4, choices=BATCH, null=True, blank=False, default='2023')

    def __str__(self):
        return self.fullname
