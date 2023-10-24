from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from djf_surveys.models import UserAnswer
from userprofile.models import ProfileList


@login_required(login_url="authentication/login")
def index(request):
    user_profile = None
    user_response = None

    user_exists = ProfileList.objects.filter(owner=request.user).exists()
    if user_exists:
        user_profile = ProfileList.objects.get(owner=request.user)

    response_exists = UserAnswer.objects.filter(user_id=request.user.id).exists()
    if response_exists:
        user_response = UserAnswer.objects.get(user_id=request.user.id)

    return render(request, "index.html", {"user_profile": user_profile,
                                          "user_response": user_response})


# def handler404(request, exception):
#     return render(request, "404.html", status=404)


# def handler500(request, *args, **argv):
#     return render(request, '400.html', status=500)
