from django.db import models
from django.conf import settings

class Group(models.Model):
  title = models.CharField(max_length=200, unique=True)
  description = models.TextField()


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
