from django.http import HttpResponse
from .scrapping import scrapping as sc

def index(request):
    return HttpResponse(sc())