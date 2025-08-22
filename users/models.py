from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The value for email is missing")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("super user must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('super user must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)

class User (AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique = True)
    #password = models.CharField(max_length =255)
    first_name = models.CharField(max_length =50)
    last_name = models.CharField(max_length =50)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]
    
    #def save(self, *args, **kwargs):
     #   if not self.pk:
     #       self.set_password(self.password)
      #  super().save(*args, **kwargs)
    def __str__(self):
        return self.email