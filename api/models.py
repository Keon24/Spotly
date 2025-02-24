from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50)
    first_name = models.CharField(max_length =50)
    last_name = models.CharField(max_length =50)
    password = models.CharField(max_length = 255)
    
    USERNAME_FIELD = "email"
    REQUIRE_FIELDS = ["first_name","last_name"]
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.email

class ParkingSpot(models.Model):
    location = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    user = models.CharField(max_length=100)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
