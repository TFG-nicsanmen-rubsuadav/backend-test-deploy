from rest_framework.response import Response
from rest_framework import views

# local imports
from .models import create_user


# TODO: Cuando estén creados los roles, a este método solo puede llamar un administrador
# el resto de usuarios se crean con el authentication de Firebase
class RegisterView(views.APIView):
    def post(self, request):
        try:
            create_user(request.data)
            return Response({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
