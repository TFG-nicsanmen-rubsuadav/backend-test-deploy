from django.http import HttpResponse

# local imports
from conf.firebase import config, firestore


def index(request):
    firestore.collection('test').document('test').set({'test': 'test'})
    return HttpResponse(f"Hello, world. You're at the main index.{config['apiKey']}")
