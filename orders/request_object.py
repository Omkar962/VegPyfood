from . import models


def requestObjectMiddleware(get_response):
    def middleware(request):

        models.request_object=request

        response=get_response(request)
        return response
    
    return middleware