from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([AllowAny])  # Anula los permisos globales
def hello_world(request):
    return Response({"message": "¡Hola mundo desde Django!"})
