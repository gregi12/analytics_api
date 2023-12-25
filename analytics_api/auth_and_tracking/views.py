from rest_framework.response import Response
from django.db.models import Count
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
import datetime
from django.db.models.functions import TruncDate
from itertools import groupby
from user_agents import parse
from rest_framework.views import APIView
from rest_framework import permissions

@api_view(['POST'])
def signup(request):
    if User.objects.filter(username=request.data['username']):
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.data['username'] is None:
        return Response({'error': 'Username cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        try:
            user = User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            return Response({'token': token.key,'user': user.username, 'url': user.url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_200_OK)
 

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def basic_info(request):
    try:
        #check which url is registered on this token
        token = request.headers['Authorization'].split()[1]
        token_obj = Token.objects.get(key=token)
        if token_obj is None:
            raise Exception('Token does not exist')
        user = token_obj.user
        user_domain = user.domain
        #get all the views for this url
        start_date = request.data['start_date']
        end_date = request.data['end_date']

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date += datetime.timedelta(days=1)
        #filter by date
        views_per_day = SiteInfo.objects.filter(time__range=(start_date, end_date)).filter(domain=user_domain).annotate(date=TruncDate('time')).values('date').annotate(views=Count('id')).order_by('date')
        if len(views_per_day) == 0:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'views': views_per_day}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def top_pages(request):
    try:

        num_pages = request.data.get('returned_pages', 10)
        if not isinstance(num_pages, int) or num_pages <= 0:
            raise Exception('Number must be positive integer')
        
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        #converting to day format
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date += datetime.timedelta(days=1)
        page_views = SiteInfo.objects.filter(time__range=(start_date, end_date)).annotate(day=TruncDate('time')).values('day', 'url').annotate(views=Count('url')).order_by('day','-views')
        if page_views is None:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)
        
        res = [[item for item in g][:num_pages] for k, g in groupby(page_views, key=lambda x: x['day'])]
        return Response(res, status=status.HTTP_200_OK)
        
    except: 
        #Not int
        if type(request.data['returned_pages']) is not int:
            raise Exception('returned_pages must be an integer')
        #Less than zero
        elif request.data['returned_pages']<=0:
            raise Exception('returned_pages must be a positive integer')



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def langauges(request):
    try:
        num_languages = request.data.get('returned_languages', 10)
        if not isinstance(num_languages, int) or num_languages <= 0:
            raise Exception('Number must be positive integer')
        #get user url by token
        token = request.headers['Authorization'].split()[1]
        token_obj = Token.objects.get(key=token)
        if token_obj is None:
            raise Exception('Token does not exist')
        user = token_obj.user
        user_domain = user.domain

        #get all the views for this url
        start_date = request.data['start_date']
        end_date = request.data['end_date']

        # Convert string dates to datetime objects and add one day to end_date
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date += datetime.timedelta(days=1)
        
        languages = SiteInfo.objects.filter(time__range=(start_date, end_date))
        languages = languages.filter(domain=user_domain).annotate(day=TruncDate('time')).values('day', 'language').annotate(views=Count('language')).order_by('day', '-views')
        # Group by day and take top languages for each day
        res = [[item for item in g][:num_languages] for k, g in groupby(languages, key=lambda x: x['day'])]

        if not res:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(res, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
   
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def entry_pages(request):
    try:
        returned_pages = request.data.get('returned_pages', 10)
        if not isinstance(returned_pages, int) or returned_pages <= 0:
            raise Exception('Number must be positive integer')

        token = request.headers['Authorization'].split()[1]
        token_obj = Token.objects.get(key=token)
        if token_obj is None:
            raise Exception('Token does not exist')
        user = token_obj.user
        domain_name = user.domain

        # Get time range
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date += datetime.timedelta(days=1)

        # Get top entry pages for this url
        entry_pages = SiteInfo.objects.filter(time__range=(start_date, end_date), url__contains=domain_name)
        entry_pages = entry_pages.exclude(http_header__contains=domain_name).annotate(day=TruncDate('time')).values('day','url').annotate(views=Count('url')).order_by('day','-views')

        # Take top pages for each day
        res = [[item for item in g][:returned_pages] for k, g in groupby(entry_pages, key=lambda x: x['day'])]

        if not res:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def browsers(request):

    try:
        returned_browsers = request.data.get('returned_browsers', 10)
        if not isinstance(returned_browsers, int) or returned_browsers <= 0:
            raise Exception('Number must be positive integer')

        token = request.headers['Authorization'].split()[1]
        token_obj = Token.objects.get(key=token)
        if token_obj is None:
            raise Exception('Token does not exist')
        user = token_obj.user
        domain_name = user.domain

        # Get time range
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date += datetime.timedelta(days=1)

        cut_time = SiteInfo.objects.filter(time__range=(start_date, end_date), url__contains=domain_name).values('user_agent_header').annotate(views=Count('user_agent_header')).order_by('-views')[:returned_browsers]
        if len(cut_time)==0:
            return Response({'error': 'No data for this date range'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_agents = []
        dicti = dict()
        all_views = 0
        for sub_dict in cut_time:
            browser = parse(sub_dict['user_agent_header']).browser.family
            user_agents.append((browser, sub_dict['views']))
            all_views += int(sub_dict['views'])

        browsers_count = Convert(user_agents, dicti)

        #counting if there are more than one user_agent for a browser and adding if so then calucalting percentage
        for key in browsers_count.keys():

            if len(browsers_count[key])>1:
                browsers_count[key] = round((sum(browsers_count[key])/all_views)*100, 2)

            elif len(browsers_count[key])==1:
                browsers_count[key] = round((int(browsers_count[key][0])/all_views)*100, 2)
            
        return Response(browsers_count, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def Convert(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request):
    try:
        boole = request.data.get('bool', None)
        if boole != 'yes':
            raise Exception('You must confirm account deletion with yes as a "bool" parameter')

        token = request.headers['Authorization'].split()[1]
        token_obj = Token.objects.get(key=token)
        if token_obj is None:
            raise Exception('Token does not exist')
        user = token_obj.user

        # Delete related SiteInfo objects
        SiteInfo.objects.filter(user_id=user.id).delete()
    
        user.delete()

        return Response("Account deleted", status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
