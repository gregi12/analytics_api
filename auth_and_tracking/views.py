from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, SiteInfoSerializer
from rest_framework import status
from .models import EmailUser as User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        try:
            user = User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            return Response({'token': token.key,'user': user.username, 'url': user.url}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_200_OK)



