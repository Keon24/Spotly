from rest_framework import serializers
from .models import ParkingLot
from .models import ParkingSpace
    
class ParkingSpaceSerializer(serializers.ModelSerializer):
        class Meta:
            model = ParkingSpace
            fields = ['id','lot','label','space_occupied','space_reserved','sensor_id']
            

class ParkingLotSerializer(serializers.ModelSerializer):
    spaces = ParkingSpaceSerializer(many=True,read_only = True)
    class Meta:
        model = ParkingLot
        fields = ['id','name','created_at','location',]
        