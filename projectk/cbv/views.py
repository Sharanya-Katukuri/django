from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentDetails
import json

# Create your views here.

@method_decorator(csrf_exempt,name='dispatch')
class DemoClass(View):
    def get(self,request):
        # return HttpResponse("hello iam get method")
        return JsonResponse({"info":"get"})
    def post(self,request):
        # return HttpResponse("hello iam post method")
        return JsonResponse({"info":"post"})
    def put(self,request):
        # return HttpResponse("hello iam put method")
        return JsonResponse({"info":"put"})
    def delete(self,request):
        # return HttpResponse("hello iam delete method")
        return JsonResponse({"info":"delete"})
    



@method_decorator(csrf_exempt,name="dispatch")
class PaymentInfo(View):
    def post(self,request):
        try:
            data=json.loads(request.body)
            payment=PaymentDetails.objects.create(order_id=data["order_id"],
                            user_email=data["email"],
                            payment_mode=data["mode"],
                            amount=data["amount"],
                            payment_status=data["status"])
            print(payment.transaction_id)
            return JsonResponse({"message":"posted successfully","transactionId":str(payment.transaction_id)},status=201)
        except Exception as e:
            return JsonResponse({"message":str(e)},status=500)