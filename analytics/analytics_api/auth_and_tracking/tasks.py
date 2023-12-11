from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import SiteInfoSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@csrf_exempt
@shared_task
def site_info(request):
    try:
        token = request.headers['Authentication']
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        url = user.url
        if url == request.data['url']:
            serializer = SiteInfoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'url does not match'}, status=status.HTTP_400_BAD_REQUEST)

