from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User (AbstractUser):
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50)
    first_name = models.CharField(max_length =50)
    last_name = models.CharField(max_length =50)

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.email