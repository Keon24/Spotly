import os
import django
os.enviromen.setdefault('DJANGO_SETTINGS_MODULE', 'spotly.settings'), django.setup()
from django.contrib.auth import get_user_model
from parking.models import ParkingSpace

User = get_user_model()

if not User.objects.filter(email='admin@mk.com').exists():
    User.objects.create_superuser(email='admin@mk.com',password='kalikali')
    print('superuser created')
    
    for i in range(1,11):
        ParkingSpace.objects.get_or_create(
        name = f"spot--[i]"
,
        defaults={'is_occupied':False},
    )
    print('parking spaces created')