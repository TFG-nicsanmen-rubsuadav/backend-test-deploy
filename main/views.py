from django.http import JsonResponse

# local imports
from .scrapping import parallel_scraping


def index(request):
    return JsonResponse(parallel_scraping(), safe=False)
