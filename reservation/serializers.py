from rest_framework import serializers 
from .models import ReservationLot


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationLot
        fields = ['user','parking','ticket_code','created_at','reserve_date','soft_delete']
        def validate(self,attrs):
            if attrs['parking'] != [attrs]:
                queryset = ReservationLot.objects.filter(parking=attrs['parking'])
            if queryset.exists():
                raise serializers.ValidationError("Parking is not Available")
            return attrs
        
            