from . import views
from django.urls import path


urlpatterns = [
    path("", views.profile, name="userprofile"),
    path("get-majors/", views.get_major, name="getmajor"),
]
