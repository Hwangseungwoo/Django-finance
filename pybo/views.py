from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import json
from collections import OrderedDict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import recommend,reco,scoring,savings,loan


def home(request):
    return render(request, 'home.html')


@csrf_exempt
def index(request):
    """
    return response
    """
    def get_data(age, gender, goal, category, type,grade):
        d1,d2,d3,d4 = recommend.final_get(age,gender,goal,category,type)
        d5 = reco.general_reco(gender,age)
        d6 = scoring.recommend_product(age, gender)
        d7 = savings.savings(age,gender)
        d8,d9,d10,d11 = loan.main_data(gender,age,grade,goal)
        return d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11
    age = request.POST['age']
    gender = request.POST['gender']
    goal = request.POST['goal']
    category = request.POST['category']
    grade = request.POST['grade']
    type = request.POST['type']
    d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11 = get_data(age,gender,goal,category,type,grade)
    new7 = d7[0][0]['KorCoNm'] +' '+ d7[0][0]['FinPrdtNm']
    new8 = d8[0][0]['KorCoNm'] +' '+ d8[0][0]['FinPrdtNm']
    new9 = d9[0][0]['KorCoNm'] +' '+ d9[0][0]['FinPrdtNm']
    new10 = d10[0][0]['KorCoNm'] +' '+ d10[0][0]['FinPrdtNm']
    new = {'obj_finan' : d1,
           'type_finan' : d2[2][0]['펀드명'],
           'obj_insur' : d3,
           'goal_insur' : d4[0][1]['상품명'],
           'obj_card' : d5[0][0],
           'obj_deposit' : d6[0][0]['상품명'],
           'obj_savings' : new7,
           'obj_loan' : new8,
           'obj_mortage' : new9,
           'obj_private_loan' : new10
           }
    

    return render(request, 'index.html', new)
