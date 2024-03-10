from django.urls import path

# local imports
from .views import *

urlpatterns = [
    path('', index, name='index'),
]
