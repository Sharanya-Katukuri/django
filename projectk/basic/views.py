from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student 
from basic.models import Post
# Create your views here.

def sample(request):
    return HttpResponse('hello world')

def sample1(request):
    return HttpResponse("welcome to django")

def sampleInfo(request):
    # data={"name":"sharanya","age":23,"city":"warangal"}
        # return JsonResponse(data)
    # data=[1,2,3]
    # return JsonResponse(data,safe=False)
    data={'result':[1,2,3]}
    return JsonResponse(data)

def dynamicresponse(request):
    name=request.GET.get("name",'sharanya')
    city=request.GET.get("city","hyd")
    return HttpResponse(f"Hello {name} from {city}")

def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})
    
@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method=='POST':
        data=json.loads(request.body)
        student=Student.objects.create(name=data.get('name'),age=data.get('age'),email=data.get('email'))
        # print(data)
        # data.get('name')
        # data.get('age')
        # data.get('email')
        return JsonResponse({"status":"success","id":student.id},status=200)

    return JsonResponse({"error":"use post method"},status=400)


@csrf_exempt
def add_post(request):
    if (request.method)=='POST':
        data=json.loads(request.body)
        post=Post.objects.create(
            post_name=data.get('post_name'),
            post_type=data.get('post_type'),
            post_date=data.get('post_date'),
            post_description=data.get('post_description')
        )
        return JsonResponse({"status":"success","message":"Post added successfully","post_id":post.id},status=201)
    return JsonResponse({"status":"error","message":"Ony POST method allowed"},status=405)
