from django.http import HttpResponse

# local imports
from conf.firebase import config, firestore
from main.scrapping import populateDB


def index(request):
    return HttpResponse(populateDB())
