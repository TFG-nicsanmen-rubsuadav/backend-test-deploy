from rest_framework.response import Response
from rest_framework import views
from rest_framework import status

# local imports
from .models import create_user, create_role


# TODO: Cuando estén creados los roles, a este método solo puede llamar un administrador
# el resto de usuarios se crean con el authentication de Firebase
class CreateUsersAdminView(views.APIView):
    def post(self, request):
        try:
            role_id = create_role(request.data['rol'])
            create_user(request.data, role_id)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
