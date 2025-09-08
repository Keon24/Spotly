from rest_framework import serializers
from .models import ReservationLot
from parking.models import ParkingSpace
import uuid

class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = ['id', 'label']

class ReservationReadSerializer(serializers.ModelSerializer):
    space = ParkingSpaceSerializer(read_only=True)
    
    class Meta:
        model = ReservationLot
        fields = ['id', 'space', 'reserve_date', 'ticket_code', 'created_at']

class DynamicParkingSpaceField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        # Ensure ParkingSpace exists, create if needed
        from parking.models import ParkingLot, ParkingSpace
        
        try:
            space_id = int(data)
        except (ValueError, TypeError):
            self.fail('incorrect_type', data_type=type(data).__name__)
        
        # Get or create parking lot
        lot, _ = ParkingLot.objects.get_or_create(
            name='Main Parking Lot',
            defaults={'location': 'Downtown', 'total_spaces': 100}
        )
        
        # Get or create parking space
        space, _ = ParkingSpace.objects.get_or_create(
            id=space_id,
            defaults={
                'lot': lot,
                'label': f'A{space_id:02d}',
                'is_occupied': False,
                'is_reserved': False,
                'sensor_id': f'sensor_{space_id}'
            }
        )
        return space


class ReservationSerializer(serializers.ModelSerializer):
    space = DynamicParkingSpaceField(queryset=ParkingSpace.objects.all())
    
    class Meta:
        model = ReservationLot
        fields = ['space', 'reserve_date']
        read_only_fields = ['ticket_code', 'user', 'created_at']

    def validate(self, attrs):
        space = attrs.get('space')  # This is now a ParkingSpace object
        reserve_date = attrs.get('reserve_date')
        user = self.context['request'].user
        
        from datetime import datetime
        from django.utils.timezone import make_aware
        sentinel_date = make_aware(datetime(1900, 1, 1))
        
        # Check if space is already reserved at this exact time
        if ReservationLot.objects.filter(space=space, reserve_date=reserve_date, soft_delete=sentinel_date).exists():
            raise serializers.ValidationError("This space is already reserved at that exact time.")

        # Check if user already has a reservation for this date (ignoring time)
        if ReservationLot.objects.filter(
            user=user, 
            reserve_date__date=reserve_date.date(), 
            soft_delete=sentinel_date
        ).exists():
            raise serializers.ValidationError("You already have a reservation for this date. Only one reservation per day is allowed.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        ticket_code = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        
        from datetime import datetime
        from django.utils.timezone import make_aware
        
        # PrimaryKeyRelatedField already converted the ID to a ParkingSpace object
        # Just create the reservation directly - no manual conversions needed
        return ReservationLot.objects.create(
            user=user, 
            ticket_code=ticket_code, 
            soft_delete=make_aware(datetime(1900, 1, 1)),
            **validated_data  # Contains space (ParkingSpace object) and reserve_date
        )
