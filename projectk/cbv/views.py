from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentDetails
import json
from .mixins import helperMixin,ResponseMixins,JsonResponseMixins

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
        




# without mixins 

# class Mixin1(View):
#     def get(self,request):
#         # return HttpResponse("hello iam from mixin1")
#         return JsonResponse({"message":"hello iam from mixin1 ","end":"All the best"})
    

# class Mixin2(View):
#     def get(self,request):
#         # return HttpResponse("hello iam from mixin2")
#         return JsonResponse({"message":"hello iam from mixin1 ","end":"All the best"})


# with mixins

class Mixin1(helperMixin,View):
    def get(self,request):
        return HttpResponse(self.greetingMessage())
        # return JsonResponse({"message":"hello iam from mixin1 ","end":self.greetingMessage()})
    

class Mixin2(helperMixin,View):
    def get(self,request):
        return HttpResponse(self.greetingMessage())
        # return JsonResponse({"message":"hello iam from mixin1 ","end":self.greetingMessage()})
    


class Products(ResponseMixins,View):
    def get(self,request):
        qp1=request.GET.get("qp1")
        name=request.GET.get("name")
        if qp1=="success":
            return self.success(name)
        else:
            return self.error(name)
        

ecommerce_data = [
    {
        "product_id": 101,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "price": 799,
        "stock": 120,
        "rating": 4.3
    },
    {
        "product_id": 102,
        "name": "Bluetooth Headphones",
        "category": "Electronics",
        "price": 2499,
        "stock": 60,
        "rating": 4.6
    },
    {
        "product_id": 103,
        "name": "Cotton T-Shirt",
        "category": "Fashion",
        "price": 599,
        "stock": 200,
        "rating": 4.1
    },
    {
        "product_id": 104,
        "name": "Running Shoes",
        "category": "Footwear",
        "price": 3999,
        "stock": 45,
        "rating": 4.5
    },
    {
        "product_id": 105,
        "name": "Stainless Steel Water Bottle",
        "category": "Home & Kitchen",
        "price": 499,
        "stock": 150,
        "rating": 4.4
    },
    {
        "product_id": 106,
        "name": "Smart Watch",
        "category": "Electronics",
        "price": 6999,
        "stock": 30,
        "rating": 4.7
    },
    {
        "product_id": 107,
        "name": "Office Chair",
        "category": "Furniture",
        "price": 8999,
        "stock": 20,
        "rating": 4.2
    },
    {
        "product_id": 108,
        "name": "Notebook Set",
        "category": "Stationery",
        "price": 299,
        "stock": 500,
        "rating": 4.0
    }
]


class getProductBycategory(JsonResponseMixins,View):
    filteredData=[]
    def get(self,request,ctg):
        print(ctg)
        for product in ecommerce_data:
            if product["category"].lower()==ctg.lower():
                self.filteredData.append(product)

        # return JsonResponse(self.filteredData,safe=False)
        return self.success(self.filteredData)