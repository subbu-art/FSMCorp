from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='my_custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='my_custom_user_permissions')
