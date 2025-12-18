from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.

def Demo(request):
    return HttpResponse("This is for testing purpose only")

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
        "price": 999,
        "stock": 150,
        "rating": 4.4
    }
]

def productById(request,id):
    for product in ecommerce_data:
        if product["product_id"]==id:
            return JsonResponse(product)
    return JsonResponse({"error":"product not found"})