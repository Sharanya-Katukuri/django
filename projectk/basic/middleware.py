class basicMiddleware:
    def __init__(self,get_response):  #to get the reponse form view as per request  #start in server
        self.get_response=get_response

    def __call__(self,request): #start when pass request
        # print(request,"hello")
        if(request.path=="/add/"):
            print(request.method,"method")
            print(request.path)
            response=self.get_response(request)
        elif(request.path=="/greet/"):
            print(request.method,"method")
            print(request.path)
            response=self.get_response(request)
        elif(request.path=="/info/"):
            print(request.method,"method")
            print(request.path)
            response=self.get_response(request)
        elif(request.path=="/post/"):
            print(request.method,"method")
            print(request.path)
            response=self.get_response(request)
        return response
        