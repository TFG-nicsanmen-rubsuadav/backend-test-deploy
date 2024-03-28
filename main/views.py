from django.http import JsonResponse

# local imports
from main.scrapping import get_restaurants


def index(request):
    return JsonResponse(get_restaurants(), safe=False)
