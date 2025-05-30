from rest_framework import serializers 
from .models import ReservationLot


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationLot
        fields = ['user','parking','ticket_code','created_at','reserve_date']
        def validate(self,attrs):
            if attrs['parking'] != [attrs]:
                queryset = ReservationLot.objects.filter(parkingq=attrs['parking'])
            if queryset.exists():
                raise serializers.ValidationError("Parking is not Available")
            return attrs
        
            