from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to = User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    expiration = models.DateTimeField()
    
    def __str__(self):
        return f'EmailVerification object {self.user.email}'