from django.db import models
from django.conf import settings

class Group(models.Model):
  title = models.CharField(max_length=200, unique=True)
  description = models.TextField()
  image = models.TextField(null=True, blank=True)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class MemberShip(models.Model):
  ROLE_CHOICES = [
      ('member', 'Member'),
      ('admin', 'Admin'),
  ]

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
  date_joined = models.DateTimeField(auto_now_add=True)

  class Meta:
      unique_together = ('user', 'group')


class MembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'group')

    def approve(self):
      self.status = 'approved'
      self.save()
      MemberShip.objects.create(user=self.user, group=self.group, role='member')

    def reject(self):
      self.status = 'rejected'
      self.save()

    def is_processed(self):
      return self.status != 'pending'


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    