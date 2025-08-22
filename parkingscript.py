import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotly.settings')
django.setup()

from django.contrib.auth import get_user_model
from parking.models import ParkingLot, ParkingSpace

User = get_user_model()

if not User.objects.filter(email='admin@mk.com').exists():
    User.objects.create_superuser(
        email='admin@mk.com',
        password='kalikali',
        first_name='Admin',
        last_name='User'
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")

lot, _ = ParkingLot.objects.get_or_create(
    name='Default Lot',
    defaults={
        'location': '123 Main St',
        'total_spaces': 10,
    }
)
NUM_SPOTS = 1000
for i in range(1, NUM_SPOTS + 1):
    ParkingSpace.objects.get_or_create(
        label=f"spot-{i}",
        lot=lot,
        defaults={
            'is_occupied': False,
            'is_reserved': False,
            'sensor_id': f"SENSOR-{i}"
        }
    )

print("Parking spaces created.")
