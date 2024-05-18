from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Group, MemberShip
from .serializers import (
  GroupSerializer,
  GroupListSerializer,
)
# Create your views here.

@api_view(['GET', 'POST'])
def group_list(request):
  print(request.user.is_authenticated)
  if request.method=="GET":
    groups = get_list_or_404(Group)
    serializer = GroupListSerializer(groups, many=True)
    return Response(serializer.data)
  elif request.method=="POST":
    # 로그인한 사용자만 그룹 생성 가능
    if not request.user.is_authenticated:
      return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      # 그룹 이름이 이미 존재하면 생성 X
      group_name = serializer.validated_data.get('title')
      if Group.objects.filter(title=group_name).exists():
          return Response({'detail': 'A group with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
      
      group = serializer.save()
      MemberShip.objects.create(user=request.user, group=group, role='admin')
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  
@api_view(['GET', 'DELETE'])
def group_detail(request, group_id):
  group = get_object_or_404(Group, pk=group_id)

  if request.method=="GET":
    serializer = GroupSerializer(group)
    return Response(serializer.data)
  elif request.method=="DELETE":
    is_admin = MemberShip.objects.filter(group=group, user=request.user, role='admin')

    if not is_admin:
      return Response({'detail': 'You do not have permission to delete this group.'}, status=status.HTTP_403_FORBIDDEN) 
    
    data = {'detail': f'Group {group.title} deleted successfully.'}
    group.delete()
    return Response(data, status=status.HTTP_204_NO_CONTENT)
