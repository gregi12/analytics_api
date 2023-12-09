from rest_framework import serializers
from .models import EmailUser, SiteInfo



class UserSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = EmailUser
        fields = ['username','url']
    
class SiteInfoSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = SiteInfo
        fields = ['ip_address','url','http_header','user_agent_header','window_width','window_height','max_touch_points','language']