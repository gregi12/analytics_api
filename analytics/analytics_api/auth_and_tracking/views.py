from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, SiteInfoSerializer
from rest_framework import status
from .models import EmailUser as User, SiteInfo
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from collections import Counter
from rest_framework.views import APIView
import json

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


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['GET'])
def basic_info(request):
    try:
        #check which url is registered on this token
        token = request.headers['Authentication']
        token_obj = Token.objects.get(key=token)
        if token_obj is None:
            raise Exception('Token does not exist')
        user = token_obj.user
        url = user.url
        #get all the views for this url
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        cut_time = SiteInfo.objects.filter(time__range=[start_date, end_date])
        if len(cut_time) == 0:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)
        views = cut_time.filter(url=url)
        num_of_views = len(views)
        dicti = {"cut_type":str(len(views))}
        return Response({'views': num_of_views, "url": url, "dict":dicti}, status=status.HTTP_200_OK)
    except:
        raise Exception('Authentication header is missing')


@csrf_exempt
@api_view(['GET'])
def top_pages(request):
    try:
        if request.data['returned_pages'] is None:
            num_pages = 10

        elif type(request.data['returned_pages']) ==  int and request.data['returned_pages']>0:
            num_pages = request.data['returned_pages']

        start_date = request.data['start_date']
        end_date = request.data['end_date']
        cut_time = SiteInfo.objects.filter(time__range=[start_date, end_date])
        if len(cut_time) == 0:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)
        list_of_urls = []
        for obj in cut_time:
            list_of_urls.append(obj.url)
        counter_Object = Counter(list_of_urls)
        return Response(counter_Object.most_common(num_pages), status=status.HTTP_200_OK)
        
    except: 
        if request.headers['Authentication'] is None:
            raise Exception('Authentication header is missing')
        
        elif type(request.data['returned_pages']) is not int:
            raise Exception('returned_pages must be an integer')

        elif request.data['returned_pages']<=0:
            raise Exception('returned_pages must be a positive integer')

       



@csrf_exempt
@api_view(['GET'])
def langauges(request):
    try:
        if request.data['returned_languages'] is None:
            num_languages = 10

        elif type(request.data['returned_languages']) ==  int and request.data['returned_languages']>0:
            num_languages = request.data['returned_languages']
       

        start_date = request.data['start_date']
        end_date = request.data['end_date']
        cut_time = SiteInfo.objects.filter(time__range=[start_date, end_date])
        if len(cut_time) == 0:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)
        list_of_languages = []
        for obj in cut_time:
            list_of_languages.append(obj.language)
        counter_Object = Counter(list_of_languages)
        return Response(counter_Object.most_common(num_languages), status=status.HTTP_200_OK)
    except:
        raise Exception('number of languages must be a positive integer')
        



