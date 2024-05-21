from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
	pass


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    embedding = models.JSONField(blank=True, null=True)