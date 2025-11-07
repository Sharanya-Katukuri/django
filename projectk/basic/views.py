from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection

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