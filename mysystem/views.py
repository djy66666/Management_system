from django.shortcuts import render, redirect,HttpResponse
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from datetime import date

from mysystem.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from mysystem.models import course, Cornellstu, anouncement, attendence, Surveytable, Surveyresult
import datetime
import json


# Create your views here.


@csrf_exempt
def home(request):
    res = []
    if request.method == "POST":
        count1 = anouncement.objects.all().count()
        count2 = Surveytable.objects.all().count()
        count3 = Cornellstu.objects.all().count()
        d = {'announcement': count1, 'survey': count2, 'stu_number': count3}
        # return render(request, 'login.html', d)
        return JsonResponse(d)
    return render(request, 'index.html')

@csrf_exempt
def admin_login(request):
    error = False
    if request.method == "POST":
        postBody = request.body
        json_result = json.loads(postBody)
        u = json_result['username']
        p = json_result['password']
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            error = True
            j = json.dumps(error)
            d = {'result': j}
            # return render(request, 'login.html', d)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'wrong'})

        # if user:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     error = True
    d = {'error': error}
    return render(request, 'login.html', d)


def viewcourse(request, id):
    # if not request.user.is_authenticated:
    #         return redirect('home')

    # data1 = Cornellstu.objects.filter(netid=id)
    # filter()返回的是QuerySet,相当于做了一次筛选，而不是返回一条实例
    data = Cornellstu.objects.get(netid=id)
    a = {'t1':data.courseinfo.time1, 't2':data.courseinfo.time2, 't3':data.courseinfo.time3}
    return JsonResponse(a)

@csrf_exempt
def viewattendence(request):
    if not request.user.is_authenticated:
        print("wrong user")
        return redirect('home')
    if request.method == "POST":
        orders = attendence.objects.all()
        dic = {}
        count = 1
        for order in orders:
            a = {'1': order.stu1, '2': order.stu2, '3': order.stu3, '4': order.stu4, '5': order.stu5, '6': order.stu6,
                 '7': order.stu7, '8': order.stu8, '9': order.stu9, '10': order.stu10}
            dic[count] = a
            count += 1
        return JsonResponse(dic)
    return render(request, 'attend.html')


@csrf_exempt
def viewtest(request):
    if not request.user.is_authenticated:
        print("wrong user")
        return redirect('home')

    orders = attendence.objects.all()
    dic = {}
    count = 1
    for order in orders:
        a = {'1': order.stu1, '2': order.stu2, '3': order.stu3, '4': order.stu4, '5': order.stu5, '6': order.stu6,
             '7': order.stu7, '8': order.stu8, '9': order.stu9, '10': order.stu10}
        dic[count] = a
        count += 1
    return JsonResponse(dic)



def viewAnnouncement(request):
    # if not request.user.is_authenticated:
    #     return redirect('home')
    data = anouncement.objects.last()
    a = {'time': data.time, 'title': data.title, 'content': data.content}
    return JsonResponse(a)


@csrf_exempt
def announce(request):
    # 这时最好显示一个请登录的提示
    if not request.user.is_authenticated:
        return redirect('home')
    error3 = False

    if request.method == "POST":

        postBody = request.body
        json_result = json.loads(postBody)
        c = json_result['content']
        t = json_result['title']

        anouncement.objects.create(title=t, content=c)
        return JsonResponse({'status': 'ok'})
    result = {'content': '123', 'title': '456'}
    c = result['content']
    t = result['title']
    anouncement.objects.create(title='t', content='c')


    return render(request, 'announce.html')


@csrf_exempt
def count_attend(request):
    if request.method == "POST":

        postBody = request.body
        json_result = json.loads(postBody)
        # for k,v in json_result.items():
        #     attendence.objects.create()
        attendence.objects.create(**json_result)
    return HttpResponse('ok')


def admin_logout(request):
    logout(request)
    return render(request, 'logout.html')

@csrf_exempt
def survey(request):
    if not request.user.is_authenticated:
        return redirect('home')
    error3 = False

    if request.method == "POST":

        postBody = request.body
        json_result = json.loads(postBody)
        d = json_result['description']
        q = json_result['Q1']

        Surveytable.objects.create(description=d, question1=q)
        Surveyresult.objects.create()
        return JsonResponse({'status': 'ok'})


    return render(request, 'survey.html')


@csrf_exempt
def sendans(request):
    if request.method == "POST":
        count = Surveyresult.objects.last()
        count.ans1 += 1
        count.save()
    return HttpResponse('ok')


@csrf_exempt
def viewresponse(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        answer = Surveyresult.objects.last()
        content = Surveytable.objects.last()
        ans = answer.ans1
        cont = content.description
        ques = content.question1
        a = {'description': cont, 'Q1': ques,  'response': ans}
        return JsonResponse(a)
    return render(request, 'response.html')


def viewquestion(request):
    # if not request.user.is_authenticated:
    #     return redirect('home')
    data = Surveytable.objects.last()
    ques = data.question1
    a = {'question': ques}
    return JsonResponse(a)

    

# def index1(request):
#     if request.method=="POST":
#         username = request.POST.get("username")
#         pwd = request.POST.get("password")
#
#         print(username)
#         print(pwd)
#
#         if username == "klvchen" and pwd=="123":
#             return HttpResponse("登录成功")
#     #return render(req, "login.html")
#     kl = "you are welcome"
#     a = "hello"
#     b = "world"
#     c = "what"
#     return render_to_response("index1.html", locals())

@csrf_exempt
def Signup(request):
    if request.method == "POST":
        postBody = request.body
        json_result = json.loads(postBody)
        f = json_result['firstname']
        l = json_result['lastname']
        u = json_result['username']
        p = json_result['password']
        e = json_result['email']
        user = User.objects.filter(username=u)
        if user:
            print("user already exists：")
            error= True
        else:
            us = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
    # test part
    # user = User.objects.filter(username="xubin")
    # if user:
    #     print("user already exists：")
    # else:
    #     User.objects.create_user(username="xubin", password="123456", email="bx83@cornell.edu", first_name='Bin', last_name='Xu')
    #     username = "xubin"
    #     password = "123456"
    #     user = authenticate(request,  username=username, password=password)
    return render(request, 'account.html')
