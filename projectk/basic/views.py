from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student 
from basic.models import Post,Users
from django.contrib.auth.hashers import make_password,check_password
import jwt
from django.conf import settings
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
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
    
    elif (request.method)=='GET':
        result=list(Student.objects.values())
        # result=tuple(Student.objects.values())
        for i in result:
            print(i)
        # print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    
        # # get all records
        # 
        # results=list(Student.objects.all().values())
        # return JsonResponse({"status":"ok","data":results},status=200)
        
        # # get a specific record by id
        # data=json.loads(request.body)
        # ref_id=data.get("id")
        # results=list(Student.objects.filter(id=ref_id).values())
        # return JsonResponse({"status":"ok","data":results},status=200)

        # filter by age >=20
        # data=json.loads(request.body)
        # ref_age=data.get("age")
        # results=list(Student.objects.filter(age__gte=ref_age).values())
        # return JsonResponse({"status":"ok","data":results},status=200)

        # # filter by age<=25
        # data=json.loads(request.body)
        # ref_age=data.get("age")
        # results=list(Student.objects.filter(age__lte=ref_age).values())
        # return JsonResponse({"status":"ok","data":results},status=200)

        # order by name
        # results=list(Student.objects.order_by('name').values())
        # return JsonResponse({"status":"ok","data":results},status=200)
    

        # get unique ages
        # results=list(Student.objects.values('age').distinct())
        # return JsonResponse({"status":"ok","data":results},status=200)

        # count total students
        # results=Student.objects.count()
        # return JsonResponse({"status":"ok","data":results},status=200)

    
    elif (request.method)=='PUT':
        data=json.loads(request.body)
        ref_id=data.get("id")#getting id
        new_email=data.get("email")#getting email
        existing_student=Student.objects.get(id=ref_id) #fetched the object as per the id
        # print(existing_student)
        existing_student.email=new_email #updating with new email
        existing_student.save()
        # updated_data=Student.objects.filter(id=ref_id).values().first()
        updated_data = list(Student.objects.filter(id=ref_id).values())

        return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)
    
    elif (request.method)=='DELETE':
        data=json.loads(request.body)
        ref_id=data.get("id")#getting id
        get_deleting_data = list(Student.objects.filter(id=ref_id).values())

        to_be_delete=Student.objects.get(id=ref_id)
        to_be_delete.delete()

        return JsonResponse({"req":"success","message":"student record delete successfully","deleted data":get_deleting_data},status=200)

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
    elif(request.method)=="GET":
        results=list(Post.objects.all().values())
        print(results)
        return JsonResponse({"status":"ok","data":results},status=200)
        
    return JsonResponse({"status":"error","message":"Ony POST method allowed"},status=405)
 


def job1(request):
    return JsonResponse({"message":"u have successfully applied for job1"},status=200)
def job2(request):
    return JsonResponse({"message":"u have successfully applied for job2"},status=200)


@csrf_exempt
def signUp(request):
    if(request.method)=="POST":
        data=json.loads(request.body)
        print(data)
        user=Users.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            password=make_password(data.get("password"))
        )
        return JsonResponse({"status":"success"},status=200)
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_username=data.get("username")
        print(ref_username)
        new_password=data.get("password")
        print(new_password)
        try:
            existing_user=Users.objects.get(username=ref_username)
        except Users.DoesNotExist:
                return JsonResponse({"status": "user not found"}, status=404)

        existing_user.password=make_password(new_password)
        existing_user.save()
        return JsonResponse({"status":"password changed successfully","username":existing_user.username},status=200)

@csrf_exempt
def login(request):
    if request.method=="POST":
        data=request.POST
        print(data)
        username=data.get('username')
        password=data.get('password')
        try:
            user=Users.objects.get(username=username)
            issed_time=datetime.now(ZoneInfo("Asia/Kolkata"))
            expired_time=issed_time+timedelta(minutes=1)
            if check_password(password,user.password):
                # token="a json web token"
                # creating jwt token
                payload={"username":username,"email":user.email,"id":user.id,"exp":expired_time}
                token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
                return JsonResponse ({"status":'successfully loggedin',"token":token,"issed_at":issed_time,"expired_at":expired_time,"expired_in":int((expired_time-issed_time).total_seconds()/60)},status=200)
            else:
                return JsonResponse({"status":"failure","message":"invalid password"},status=400)
        except Users.DoesNotExist:
            return JsonResponse({"status":"failure","message":"user not found"},status=400)
    

@csrf_exempt
def change_password(request):
    if request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        new_password=data.get("password")
        existing_user=Users.objects.get(id=ref_id)
        existing_user.password=make_password(new_password)
        existing_user.save()
        return JsonResponse({"status":"change the password successfully","username":existing_user.username},status=200)

@csrf_exempt
def check(request):
    hased_data="pbkdf2_sha256$870000$5roUXT141gfhgJ5OpoesMN$+cGP0UO6JPJy2yWeMC6nIqrnKjOB1/2eD2prUwA4fAk="
    ipdata=request.POST
    print(ipdata)
    # hased_data=make_password(ipdata.get("ip"))
    x=check_password(ipdata.get("ip"),hased_data)
    print(x)
    # print(hased_data)
    return JsonResponse({"status":"success","data":x},status=200)
