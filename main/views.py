from django.http import JsonResponse

# local imports
from .populateDB import PopulateDatabase


def index(request):
    initialize_populate = PopulateDatabase()
    return JsonResponse((initialize_populate.populate()), safe=False)
