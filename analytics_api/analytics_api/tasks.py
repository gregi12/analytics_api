from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from auth_and_tracking.serializers import SiteInfoSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from celery import Celery
from urllib.parse import urlparse
from auth_and_tracking.models import SiteInfo
from auth_and_tracking.serializers import SiteInfoSerializer
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator



@shared_task
def site_info(req):
    data_dict = {
    'user_id': req.user.id,
    'url': req.data['url'],
    'ip_address': req.data['ip_address'],
    'http_header': req.data['http_header'],
    'user_agent_header': req.data['user_agent_header'],
    'window_width': req.data['window_width'],
    'window_height': req.data['window_height'],
    'max_touch_points': req.data['max_touch_points'],
    'language': req.data['language']
}
    serializer = SiteInfoSerializer(data=data_dict)
    if serializer.is_valid():
        serializer.save()


@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    try:
        token = request.headers['Authorization'].split()[1]
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        domain = user.domain
        parsed_request_url = urlparse(request.data['url'])
        req_domain = parsed_request_url.netloc
        if domain == req_domain:
            site_info(request)
        else:
            return Response({'error': 'invalid url'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"domain":domain}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
 


