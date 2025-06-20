from django.db import models
from django.contrib.auth import get_user_model
from parking.models import ParkingSpace
from .models import get_user_model
# Create your models here.
class ReservationLot(models.Model):
    space = models.ForeignKey(ParkingSpace,on_delete=models.CASCADE)
    user = models. ForeignKey(get_user_model(),on_delete=models.CASCADE)
    ticket_code = models.CharField(max_length = 255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reserve_date = models.DateTimeField(auto_now_add=True)
    soft_delete = models.DateTimeField(auto_now_add=True)
    is_occupied = models.BooleanField(default=False)
    
   