from django.urls import path

# local imports
from .views import CreateUsersAdminView

urlpatterns = [
    path('create/', CreateUsersAdminView.as_view()),
]
