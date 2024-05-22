import json
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.S3ImageUploader import S3ImageUploader

from .models import Group, MemberShip, MembershipRequest, Post, Comment
from .serializers import (
    GroupSerializer,
    GroupListSerializer,
    MembershipRequestSerializer,
    MembershipRequestListSerializer,
    MembershipListSerializer,
    PostSerializer,
    PostListSerializer,
    CommentSerializer,
)

from movies.serializers import (
    MovieListSerializer
)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def group_list(request):
    if request.method == "GET":
        groups = Group.objects.all()

        if not groups:
            return Response({"detail": "No groups available"})

        serializer = GroupListSerializer(groups, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # 로그인한 사용자만 그룹 생성 가능
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # uploader = S3ImageUploader()

        image = request.FILES.get('image')

        if image:
            image_url = uploader.upload_image(image, image.content_type)
        else:
            image_url = None

        print(image_url)
        print(type(image_url))

        serializer = GroupSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            # 그룹 이름이 이미 존재하면 생성 X
            group_name = serializer.validated_data.get("title")
            if Group.objects.filter(title=group_name).exists():
                return Response(
                    {"detail": "A group with this name already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            group = serializer.save(image = image_url)

            MemberShip.objects.create(user=request.user, group=group, role="admin")
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_group_list(request):
    if request.method == "GET":
        memberships = MemberShip.objects.filter(user=request.user)
        serializer = MembershipListSerializer(memberships, many=True)
        return Response(serializer.data)


@api_view(["GET", "DELETE", "PUT"])
def group_detail(request, group_id):
    print(group_id)
    group = get_object_or_404(Group, pk=group_id)

    if request.user.is_authenticated:
        is_group_admin = MemberShip.objects.filter(
            group=group, user=request.user, role="admin"
        ).exists()

    if request.method == "GET":
        serializer = GroupSerializer(group, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PUT":
        if not is_group_admin:
            return Response(
                {"detail": "You do not have permission to edit this group."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        if not is_group_admin:
            return Response(
                {"detail": "You do not have permission to delete this group."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = {"detail": f"Group {group.title} deleted successfully."}
        group.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def membership_request_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    is_group_admin = MemberShip.objects.filter(
        group=group, user=request.user, role="admin"
    ).exists()

    if request.method == "GET":
        # 그룹 관리자가 아니면 확인 X
        if not is_group_admin:
            return Response(
                {"detail": "You do not have permission to get membership requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        membership_requests = MembershipRequest.objects.filter(
            group=group, status="pending"
        )
        serializer = MembershipRequestListSerializer(membership_requests, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        is_request_exist = MembershipRequest.objects.filter(
            user=request.user, group=group
        ).exists()
        # 이미 가입신청한 그룹에 또 신청할 수 없음
        if is_request_exist:
            return Response(
                {"detail": "Membership request already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MembershipRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def membership_request_detail(request, group_id, membership_request_id):
    group = get_object_or_404(Group, pk=group_id)
    is_group_admin = MemberShip.objects.filter(
        group=group, user=request.user, role="admin"
    ).exists()
    print(is_group_admin)

    if request.method == "PATCH":
        # 그룹의 관리자가 아니면 요청 변경 불가
        if not is_group_admin:
            return Response(
                {
                    "detail": "You do not have permission to edit this membership request."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        membership_request = get_object_or_404(
            MembershipRequest, pk=membership_request_id
        )

        # 이미 처리된 신청은 다시 처리 X
        if membership_request.is_processed():
            return Response(
                {"detail": "This membership request has already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        approval = json.loads(request.data.get("approval"))

        if approval:
            membership_request.approve()
            data = {"detail": "Membership request approved successfully"}
        else:
            membership_request.reject()
            data = {"detail": "Membership request rejected"}

        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def group_leave(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    membership = get_object_or_404(MemberShip, group=group, user=request.user)

    if membership.role == "admin":
        return Response(
            {"detail": "Group admin cannot leave the group."},
            status=status.HTTP_403_FORBIDDEN,
        )

    membership.delete()

    return Response(
        {"detail": "You have left the group successfully."},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def group_like_movie_list(request, group_id):
    if request.method == "GET":        
        group = get_object_or_404(Group, pk=group_id)
        memberships = MemberShip.objects.filter(group=group)

        group_like_movies = []

        for membership in memberships:
            print(membership.user)
            user_like_movies = membership.user.like_movies.all()
            print(user_like_movies)
            group_like_movies.extend(user_like_movies)
            
        
        group_like_movies = list(set(group_like_movies))
        serializer = MovieListSerializer(group_like_movies, many=True)
        
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def group_post_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if request.method == "GET":
        posts = Post.objects.filter(group=group)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # 그룹의 멤버가 아니면 작성 X
        is_member = MemberShip.objects.filter(user=request.user).exists()

        if not is_member:
            return Response({'detail': 'only group member can write posts'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 게시물 작성
            serializer.save(user=request.user, group=group)
            return Response(serializer.data)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def group_post_detail(request, group_id, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if not post.user == request.user:
        return Response({"detail": "You do not have permission to handle this post."} ,status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({'detail': 'post deleted successfully'})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def group_comment_list(request, group_id, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data)

@api_view(["PUT" ,"DELETE"])
@permission_classes([IsAuthenticated])
def group_comment_detail(request, group_id, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user != comment.user:
        return Response({"detail": "You do not have permission to handle this comment."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == "DELETE":
        if request.user == comment.user:
            comment.delete()
            return Response({'detail': 'comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        