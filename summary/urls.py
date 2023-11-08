from . import views
from django.urls import path
from djf_surveys.admins import views as admin_views


urlpatterns = [
    path("", views.summary, name="summary"),
    path("surveys/dashboard/", admin_views.AdminSurveyListView.as_view(), name="dashboard"),
    path("get-user-score/<int:pk>/", views.get_user_score, name="getuserscore"),
]
