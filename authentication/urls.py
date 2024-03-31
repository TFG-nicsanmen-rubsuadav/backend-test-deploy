from django.urls import path

# local imports
from .views import RegisterView

urlpatterns = [
    path('create/', RegisterView.as_view()),
]
