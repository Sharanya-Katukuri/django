from django.http import JsonResponse
import re,json
from basic.models import Users


class basicMiddleware:
    def __init__(self, get_response):  #automatically give the response #start the server then it is run

        self.get_response=get_response

    def __call__(self,request): #start when pass request
        print(request,"hello")
        if(request.path=="/add/"):
            print(request.method,"method")
            print(request.path)
        elif(request.path=="/greet/"):
            print(request.method,"method")
            print(request.path)
        elif(request.path=="/info/"):
            print(request.method,"method")
            print(request.path)
        elif(request.path=="/post/"):
            print(request.method,"method")
            print(request.path)
        response= self.get_response(request)
        return response

# class basicMiddleware: #class in camel case
#     def _init_(self,get_response):
#         self.get_response=get_response
#     def _call_   (self,request):
#         data=json.loads(request.body)
#         username=data.get("username") 
#         email=data.get("email")
#         dob=data.get("dob")
#         password=data.get("pswd")
        # check the username rules with regex
        # check the email rules with regex
        # check dob rules with regex
        # check the password with regex


class sscMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=request.GET.get("ssc")
            if(ssc_result!='True'):
                return JsonResponse({
                   "error":"u should qualify atleast ssc for applying this job"
               },status=400)
        return self.get_response(request)


class MedicalFitMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path=="/job1/"):
            medical_fit_result=request.GET.get("medically_fit")
            if(medical_fit_result !='True'):
                 return JsonResponse({
                   "error":"medically unfit for this job"
               },status=400)
        return self.get_response(request)
        
        

class AgeMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            age_checker=int(request.GET.get("age",17))
            if not (18 <= age_checker <= 25):
                return JsonResponse({"error":"age must be in between 18 and 25"},status=400)
        return self.get_response(request)
        
                
        
# username
# email
# password

# rules: username
# should be unique
# must be 3-20 characters
# cannot statrs with or ends with .,_
# cannot have .. or __
# no spaces
# should contains letters,numbers,dot,underscore


class UsernameMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path=="/signup/"):
            data=json.loads(request.body)

            username=data.get("username","")
            # checks username is empty or name 
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            # checks length
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should contains 3 to 20 characters"},status=400)
            # checks starting and ending
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not starts or ends with . or _"},status=400)
            # checks allowed characters
            if not re.match(r"^[a-zA-z0-9._]+$",username):
                return JsonResponse({"error":"username should contains letters,numbers,dot,underscore"},status=400)
            # checks .. and __
            if ".." in username or "__" in username:
                return JsonResponse({"error":"cannot have .. or __"},status=400)
        return self.get_response(request)   
            


# email should not empty
# basic email pattern
# if duplicate email found --->show  email already exists

class EmailMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path=="/signup/"):
            data=json.loads(request.body)
            Email=data.get("email","")
            if not Email:
                return JsonResponse({"error":"email should not empty"},status=400)
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', Email):
                return JsonResponse({"error":"Invalid email format. Email must contain '@' and a valid domain"
},status=400)
            if Users.objects.filter(email=Email).exists():
                return JsonResponse({"error": "email already exists"}, status=400)

        return self.get_response(request)

# not empty password
# strong password pattern

class PasswordMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path=="/signup/"):
            data=json.loads(request.body)
            password=data.get("password","")
            if not password:
                return JsonResponse({"error":"password should not empty"},status=400)
            if len(password)<8 or len(password)>12:
                return JsonResponse({"error":"password should contains 8 to 12 characters"},status=400)
            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$', password):
                   return JsonResponse({"error": "Password must include uppercase, lowercase, digit, special character"},status=400)
        return self.get_response(request)




   
