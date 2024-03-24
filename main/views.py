from django.http import HttpResponse

# local imports
from main.scrapping import populateDB


def index(request):
    return HttpResponse(populateDB())
