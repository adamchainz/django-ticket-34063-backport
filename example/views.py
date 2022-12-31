from django.http import HttpResponse


async def index(request):
    if "x" in request.POST:
        pass
    return HttpResponse("hi")
