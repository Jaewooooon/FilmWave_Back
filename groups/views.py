import json
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Group, MemberShip, MembershipRequest
from .serializers import (
  GroupSerializer,
  GroupListSerializer,
  MembershipRequestSerializer,
  MembershipRequestListSerializer,
)

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
  
@api_view(['GET', 'DELETE', 'PUT'])
def group_detail(request, group_id):
  print(group_id)
  group = get_object_or_404(Group, pk=group_id)

  if request.user.is_authenticated:
    is_group_admin = MemberShip.objects.filter(group=group, user=request.user, role='admin').exists()

  if request.method=="GET":
    serializer = GroupSerializer(group)
    return Response(serializer.data)
  
  elif request.method=="PUT":
    if not is_group_admin:
      return Response({'detail': 'You do not have permission to edit this group.'}, status=status.HTTP_403_FORBIDDEN) 
    
    serializer = GroupSerializer(group, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)
    
  elif request.method=="DELETE":
    if not is_group_admin:
      return Response({'detail': 'You do not have permission to delete this group.'}, status=status.HTTP_403_FORBIDDEN) 
    
    data = {'detail': f'Group {group.title} deleted successfully.'}
    group.delete()
    return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def membership_request_list(request, group_id):
  group = get_object_or_404(Group, pk=group_id)

  is_group_admin = MemberShip.objects.filter(group=group, user=request.user, role='admin').exists()

  if request.method=="GET":
    # 그룹 관리자가 아니면 확인 X
    if not is_group_admin:
      return Response({'detail': 'You do not have permission to get membership requests.'}, status=status.HTTP_403_FORBIDDEN) 

    membership_requests = MembershipRequest.objects.filter(group=group, status='pending')
    serializer = MembershipRequestListSerializer(membership_requests, many=True)

    return Response(serializer.data)
    
    
  elif request.method=="POST":
    is_request_exist = MembershipRequest.objects.filter(user=request.user, group=group).exists()
    # 이미 가입신청한 그룹에 또 신청할 수 없음
    if is_request_exist:
      return Response({'detail': 'Membership request already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MembershipRequestSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save(user=request.user, group=group)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def membership_request_detail(request, group_id, membership_request_id):
  group = get_object_or_404(Group, pk=group_id)
  is_group_admin = MemberShip.objects.filter(group=group, user=request.user, role='admin').exists()
  print(is_group_admin)

  if request.method=="PATCH":
    # 그룹의 관리자가 아니면 요청 변경 불가
    if not is_group_admin:
      return Response({'detail': 'You do not have permission to edit this membership request.'}, status=status.HTTP_403_FORBIDDEN) 

    membership_request = get_object_or_404(MembershipRequest, pk=membership_request_id)
    
    # 이미 처리된 신청은 다시 처리 X
    if membership_request.is_processed():
      return Response({'detail': 'This membership request has already processed'}, status=status.HTTP_400_BAD_REQUEST)

    approval = json.loads(request.data.get('approval'))

    if approval:
      membership_request.approve()
      data = {'detail': 'Membership request approved successfully'}
    else:
      membership_request.reject()
      data = {'detail': 'Membership request rejected'}

    return Response(data, status=status.HTTP_204_NO_CONTENT)
