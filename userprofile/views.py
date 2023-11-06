from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FacultyList, MajorList, ProfileList
from django.http import JsonResponse
from djf_surveys.models import UserAnswer
from .forms import EditProfile


@login_required(login_url="authentication/login")
def profile(request):
    user_profile = None
    user_response = None

    user_exists = ProfileList.objects.filter(owner=request.user).exists()
    if user_exists:
        user_profile = ProfileList.objects.get(owner=request.user)

    response_exists = UserAnswer.objects.filter(user_id=request.user.id).exists()
    if response_exists:
        user_response = UserAnswer.objects.get(user_id=request.user.id)

    faculties = FacultyList.objects.all()

    if request.method == "GET":
        form = EditProfile(instance=user_profile)
        context = {
            "faculties": faculties,
            "user_profile": user_profile,
            "user_response": user_response,
            "form": form,
        }
        return render(request, "userprofile/profile.html", context)
    else:
        form = EditProfile(request.POST, instance=user_profile)
        if user_exists:
            user_profile.fullname = form.data["fullname"]
            user_profile.gender = form.data["gender"]
            user_profile.nim = form.data["nim"]
            user_profile.faculty = FacultyList.objects.get(pk=form.data["faculty"])
            user_profile.major = MajorList.objects.get(pk=form.data["major"])
            user_profile.batch = form.data["batch"]
            user_profile.save()
        else:
            ProfileList.objects.create(
                owner = request.user,
                fullname =form.data["fullname"],
                gender = form.data["gender"],
                nim = form.data["nim"],
                faculty = FacultyList.objects.get(pk=form.data["faculty"]),
                major = MajorList.objects.get(pk=form.data["major"]),
                batch = form.data["batch"],
            )
        messages.success(request, "Data telah disimpan")
        return redirect("userprofile")


def get_major(request):
    faculty_id = request.GET.get("faculty")

    faculty = FacultyList.objects.filter(id=faculty_id)
    majors = list(MajorList.objects.filter(faculty__in=faculty).values("major"))
    majors_id = list(MajorList.objects.filter(faculty__in=faculty).values("id"))
    response_data = {"majors": majors, "majors_id": majors_id}

    return JsonResponse(response_data)
