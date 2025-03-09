from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    DoesNotExist = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)