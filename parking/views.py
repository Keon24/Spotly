from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from .models import ParkingSpace, ParkingLot
from .serializers import ParkingSpaceSerializer, ParkingLotSerializer
# Create your views here.
class AvailableParkingSpacesView(ListAPIView):
    queryset = ParkingSpace.objects.filter(is_occupied=False)
    serializer_class = ParkingSpaceSerializer
    
    
class ParkingLotListView(ListAPIView):
    queryset = ParkingLot.objects.all()
    lot_serializer = ParkingLotSerializer


def setup_parking_spaces(request):
    """
    Create parking lots and spaces - can be called via URL
    """
    # Create a parking lot first
    lot, lot_created = ParkingLot.objects.get_or_create(
        name='Main Parking Lot',
        defaults={
            'location': '123 Main St, Downtown',
            'total_spaces': 20
        }
    )

    # Create parking spaces
    spaces_created = 0
    for i in range(1, 21):  # Create 20 spaces
        space, created = ParkingSpace.objects.get_or_create(
            lot=lot,
            label=f'A{i:02d}',
            defaults={
                'is_occupied': False,
                'is_reserved': False,
                'sensor_id': f'sensor_{i}'
            }
        )
        if created:
            spaces_created += 1

    total_spaces = ParkingSpace.objects.count()
    
    return JsonResponse({
        'success': True,
        'message': f'Setup complete! Created {spaces_created} new parking spaces.',
        'parking_lot_created': lot_created,
        'total_spaces': total_spaces
    })