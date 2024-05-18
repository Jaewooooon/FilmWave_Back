from rest_framework import serializers
from .models import Group, MemberShip, MembershipRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class GroupSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

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
    
    def get_members(self, obj):
        members = MemberShip.objects.filter(group=obj).select_related('user')
        return UserSerializer([member.user for member in members], many=True).data
    

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


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'
        read_only_fields = ('user', 'group',)


class MembershipRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'
