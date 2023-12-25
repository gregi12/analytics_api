# Create your tests here.
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import EmailUser as User
import datetime
class SignupTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
        
    def test_signup(self):
    # Test successful signup
        data = {
            'url': 'http://www.example.com/',
            'username': 'lepiejsiepierdolnac@o2.pl',
        }
        response = self.client.post('/signup/', data=json.dumps(data), content_type='application/json')
        print(response.data)  # Print the response data to help debug
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='lepiejsiepierdolnac@o2.pl')
        self.assertIsNotNone(user)
        token_obj = Token.objects.get(user=user)
        self.assertEqual(response.data, {'token': token_obj.key, 'user':user.username ,'url': user.url})

        # Test signup with existing username
        data = {
            'url': 'http://www.example.com/',
            'username': 'lepiejsiepierdolnac@o2.pl',
        }
        response = self.client.post('/signup/', data=json.dumps(data), content_type='application/json')
        print(response.data)  # Print the response data to help debug
        self.assertEqual(response.status_code, 400)  # or whatever your application returns in this case

        # Test signup with invalid data
        data = {
            'username': '',
            'url': 'http://www.example.com/',
        }
        response = self.client.post('/signup/', data=json.dumps(data), content_type='application/json')
        print(response.data)  # Print the response data to help debug
        self.assertEqual(response.status_code, 200)  # or whatever your application returns in this case

         # Test signup with no url
        data = {
            'username': 'sprawdzto@o2.pl',
            'url': '',
        }
        response = self.client.post('/signup/', data=json.dumps(data), content_type='application/json')
        print(response.data)  # Print the response data to help debug
        self.assertEqual(response.status_code, 200)  # or whatever your application returns in this case

class AuthyTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        data = {
            'url': 'http://wp.pl/',
            'username': 'tescik@o2.pl',
        }
        response = self.client.post('/signup/', data=json.dumps(data), content_type='application/json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        print('Token ' + response.data['token'],'siema')

        data = {"url":"https://wp.pl/","ip_address":"8.8.8.8","http_header":"https://siemanko1212.pl/siemasz/","user_agent_header":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","window_width":23,"window_height":25,"max_touch_points":12,"language":"portugalski"}
        for i in range(0,5):
            response = self.client.post('/site_info/',data=json.dumps
            (data), content_type='application/json')
            print(response.data)
    
    def test_basic_info(self):
        # Test 10 good requests 
        user = User.objects.get(username='tescik@o2.pl')
        print(user.username)
        #and get basic info about user
        start_date = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d")
        end_date = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d")

        data = {"start_date":"2023-12-20","end_date":"2023-12-28"}
        print(data)
        response = self.client.get('/languages/', data=json.dumps(data))
        print(response.data)
        self.assertEqual(response.status_code, 200)