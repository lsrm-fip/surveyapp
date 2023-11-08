from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User
from userprofile.models import ProfileList
from djf_surveys.models import UserAnswer, Answer
from django.db.models import Count
from json import dumps
import numpy as np
from django.http import JsonResponse
from statistics import mean 


def cal_avg_response(user_answer_id):
    labels = ["tidak_mampu_-_1","kurang_mampu_-_2","cukup_mampu_-_3","mampu_-_4","sangat_mampu_-_5","sepenuhnya_mampu_-_6",]
    res = np.array([])
    for i in range(1, 14, 2):
        data = []
        for label in labels:
            count = Answer.objects.filter(question_id__in=[i, i + 1],user_answer_id__in=user_answer_id,value=label,).count()
            data.append(count)
        weight = np.array([[1], [2], [3], [4], [5], [6]])
        avg = np.dot(data, weight) / (2 * len(user_answer_id))
        res = np.append(res, avg)
    return res


@login_required(login_url="authentication/login")
def summary(request):
    # Info Card 1
    respondent_id_all = UserAnswer.objects.all().values_list("user_id")
    respondent_obj_all = ProfileList.objects.filter(owner_id__in=respondent_id_all)
    gender_L = respondent_obj_all.filter(gender="L")
    gender_P = respondent_obj_all.filter(gender="P")

    # Info Card 2
    unique_faculty = respondent_obj_all.values("faculty_id").annotate(total=Count("faculty_id"))

    # Info Card 3
    unique_major = respondent_obj_all.values("major_id").annotate(total=Count("major_id"))

    # Radar Chart Card
    user_answer_id_all = UserAnswer.objects.all().values_list("id")
    avg_score = cal_avg_response(user_answer_id=user_answer_id_all).tolist()

    user_id = []
    user_score_all = []
    user_avg_score = []
    for i in range(user_answer_id_all.count()):
        id = getattr(UserAnswer.objects.all()[i], "id")

        uid = getattr(UserAnswer.objects.get(id=id), "user_id")
        user_id.append(uid)
        user_fullname = str(getattr(ProfileList.objects.get(owner_id=uid), "fullname"))
        user_nim = str(getattr(ProfileList.objects.get(owner_id=uid), "nim"))

        user_answer_id = []
        user_answer_id = np.append(user_answer_id, UserAnswer.objects.get(id=id))
        user_score = cal_avg_response(user_answer_id=user_answer_id).tolist()
        user_avg_score.append(round(mean(user_score),2))

        item = {"fullname": user_fullname, "nim": user_nim, "score": user_score}
        user_score_all.append(item)
    userScoreAllJSON = dumps(user_score_all)

    # Query User Profile
    user_profile_all = ProfileList.objects.filter(owner_id__in=user_id)
    user_profile_all_list = list(user_profile_all)
    user_profile_all_list.sort(key=lambda profile:  user_id.index(profile.owner_id))
    ziplist = zip(user_profile_all_list, user_avg_score)



    state = getattr(User.objects.get(id=request.user.id), "is_superuser")
    super_user_score = [0, 0, 0, 0, 0, 0]
    if state == True:
        user_score = super_user_score
    else:
        user_answer_id = []
        user_answer_id = np.append(user_answer_id, UserAnswer.objects.get(user_id=request.user.id))
        user_score = cal_avg_response(user_answer_id=user_answer_id).tolist()

    # Contruct For Summary
    construct = [
        "Ketenangan",
        "Komitmen",
        "Kontrol",
        "Koordinasi",
        "Empati",
        "Kegigihan",
        "Adaptasi",
    ]

    # Faculty Proportion Card
    faculty_proportion = []
    faculties = ["FIP", "FBS", "FIS", "FMIPA", "FT", "FIK", "FE"]
    for i in range(unique_faculty.count()):
        id = unique_faculty[i].get("faculty_id")
        item = {"name": faculties[id - 1], "value": unique_faculty[i].get("total")}
        faculty_proportion.append(item)
    facultyProportionJSON = dumps(faculty_proportion)
    
    # Check Object Existance
    user_profile = None
    user_response = None
    user_exists = ProfileList.objects.filter(owner=request.user).exists()
    if user_exists:
        user_profile = ProfileList.objects.get(owner=request.user)
    response_exists = UserAnswer.objects.filter(user_id=request.user.id).exists()
    if response_exists:
        user_response = UserAnswer.objects.get(user_id=request.user.id)

    context = {
        "jumlah_partisipan": respondent_id_all.count(),
        "jumlah_laki_laki": gender_L.count(),
        "jumlah_perempuan": gender_P.count(),
        "jumlah_fakultas": unique_faculty.count(),
        "jumlah_jurusan": unique_major.count(),

        "skor_rata_rata": avg_score,
        "skor_anda": user_score,
        "user_score_all": userScoreAllJSON,
        "user_avg_score": user_avg_score,

        "konstruk": construct,

        "proporsi_fakultas": facultyProportionJSON,

        "user_profile_all": user_profile_all,
        "user_profile": user_profile,
        "user_response": user_response,

        "ziplist": ziplist
    }

    return render(request, "summary/summary.html", context)


def get_user_score(request, pk):
    user_answer_id = []
    a = getattr(ProfileList.objects.get(id=pk),"owner_id")
    b = getattr(UserAnswer.objects.get(user_id=a),"id")
    user_answer_id = np.append(user_answer_id, b)
    user_score = cal_avg_response(user_answer_id=user_answer_id).tolist()
    response_data = {"skor": user_score}

    return JsonResponse(response_data) 
