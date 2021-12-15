from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import json
from collections import OrderedDict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import recommend,reco,scoring,savings,loan

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
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    age = body['age']
    gender = body['gender']
    goal = body['goal']
    category = body['category']
    grade = body['grade']
    type = body['type']
    d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11 = get_data(age,gender,goal,category,type,grade)
    new = {'obj_finan' : d1,
           'type_finan' : d2,
           'obj_insur' : d3,
           'goal_insur' : d4,
           'obj_card' : d5,
           'obj_deposit' : d6,
           'obj_savings' : d7,
           'obj_loan' : d8,
           'obj_mortage' : d9,
           'obj_private_loan' : d10,
           'obj_midinterest_loan' : d11
           }
    

    return JsonResponse(new)
