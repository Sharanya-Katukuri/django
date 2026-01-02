from django.http import JsonResponse

class helperMixin:
    def greetingMessage(self):
        return  "All the best"
    
class ResponseMixins:
    def success(self,name):
        return JsonResponse({"message":f"successfully done for the request came from {name}"})
    def error(self,name):
        return JsonResponse({"message":f"some error occured for the request came from {name}"})
    
class JsonResponseMixins:
    def success(self,data):
        return JsonResponse({"status":"ok","message":"record fetched successfully","result":data})
    def error(self):
        return JsonResponse({"status":"error","message":"something went wrong"})