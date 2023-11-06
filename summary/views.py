from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User
from userprofile.models import FacultyList, ProfileList
from djf_surveys.models import UserAnswer, Answer, Question
from django.db.models import Count
from json import dumps
import numpy as np


def get_value(S, i):
    try:
        return S[i]
    except IndexError:
        return 0


def get_int(list):
    res = [int(i) for i in (str(list)).split() if i.isdigit()]
    return res


def cal_avg_response(user_answer_id):
    labels = [
        "tidak_mampu_-_1",
        "kurang_mampu_-_2",
        "cukup_mampu_-_3",
        "mampu_-_4",
        "sangat_mampu_-_5",
        "sepenuhnya_mampu_-_6",
    ]
    res = np.array([])
    for i in range(1, 14, 2):
        data = []
        for label in labels:
            count = Answer.objects.filter(
                question_id__in=[i, i + 1],
                user_answer_id__in=user_answer_id,
                value=label,
            ).count()
            data.append(count)
        weight = np.array([[1], [2], [3], [4], [5], [6]])
        avg = np.dot(data, weight) / (2 * len(user_answer_id))
        res = np.append(res, avg)
    return res


@login_required(login_url="authentication/login")
def summary(request):
    respondent_id = UserAnswer.objects.all().values_list("user_id")
    respondent_obj = ProfileList.objects.filter(owner_id__in=respondent_id)

    gender_L = respondent_obj.filter(gender="L")
    gender_P = respondent_obj.filter(gender="P")

    faculty_proportion = []
    faculties = ["FIP", "FBS", "FIS", "FMIPA", "FT", "FIK", "FE"]
    unique_faculty = respondent_obj.values("faculty_id").annotate(
        total=Count("faculty_id")
    )

    for i in range(unique_faculty.count()):
        id = unique_faculty[i].get("faculty_id")
        item = {"name": faculties[id - 1], "value": unique_faculty[i].get("total")}
        faculty_proportion.append(item)
    facultyProportionJSON = dumps(faculty_proportion)

    unique_major = respondent_obj.values("major_id").annotate(total=Count("major_id"))

    user_answer_id_all = UserAnswer.objects.all().values_list("id")
    avg_score = cal_avg_response(user_answer_id=user_answer_id_all).tolist()
    super_user_score = [0, 0, 0, 0, 0, 0]
    state = getattr(User.objects.get(id=request.user.id), "is_superuser")
    if state == True:
        user_score = super_user_score
    else:
        user_answer_id = []
        user_answer_id = np.append(
            user_answer_id, UserAnswer.objects.get(user_id=request.user.id)
        )
        user_score = cal_avg_response(user_answer_id=user_answer_id).tolist()

    user_id = UserAnswer.objects.all().values('user_id')
    user_profile = ProfileList.objects.filter(id__in = user_id)

    construct = [
        "Ketenangan",
        "Komitmen",
        "Kontrol",
        "Koordinasi",
        "Empati",
        "Kegigihan",
        "Adaptasi",
    ]

    context = {
        "jumlah_partisipan": respondent_id.count(),
        "jumlah_fakultas": unique_faculty.count(),
        "jumlah_jurusan": unique_major.count(),
        "jumlah_laki_laki": gender_L.count(),
        "jumlah_perempuan": gender_P.count(),
        "proporsi_fakultas": facultyProportionJSON,
        "skor_rata_rata": avg_score,
        "skor_anda": user_score,
        "konstruk": construct,
        "user_profile": user_profile
    }
    
    return render(request, "summary/summary.html", context)
