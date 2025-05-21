from rest_framework.generics import ListAPIView
from .models import ParkingSpace, ParkingLot
from .serializers import ParkingSpaceSerializer, ParkingLotSerializer
# Create your views here.
class AvailableParkingSpacesView(ListAPIView):
    queryset = ParkingSpace.objects.filter(is_occupied=False)
    serializer_class = ParkingSpaceSerializer
    
    
class ParkingLotListView(ListAPIView):
    queryset = ParkingLot.objects.all()
    lot_serializer = ParkingLotSerializer
    