from django.urls import path

# local imports
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
