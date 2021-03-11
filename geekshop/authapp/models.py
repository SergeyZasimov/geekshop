from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar',blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст')
