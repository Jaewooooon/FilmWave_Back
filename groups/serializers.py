from rest_framework import serializers
from .models import Group, MemberShip
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupListSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'
        
    def get_admin(self, obj):
        admin = MemberShip.objects.filter(group=obj, role='admin').select_related('user').first()
        if admin:
            return UserSerializer(admin.user).data
        return None
    
    def get_members_count(self, obj):
        return MemberShip.objects.filter(group=obj).count()

