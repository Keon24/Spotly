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

class ReservationSerializer(serializers.ModelSerializer):
    space = serializers.IntegerField()  # Accept integer space ID from frontend
    
    class Meta:
        model = ReservationLot
        fields = ['space', 'reserve_date']
        read_only_fields = ['ticket_code', 'user', 'created_at']

    def validate(self, attrs):
        space = attrs.get('space')
        reserve_date = attrs.get('reserve_date')
        user = self.context['request'].user

        # Handle integer space ID for dynamic spots
        space_id = space if isinstance(space, int) else space.id if space else None
        
        from datetime import datetime
        from django.utils.timezone import make_aware
        sentinel_date = make_aware(datetime(1900, 1, 1))
        
        # Check if space is already reserved at this exact time
        if ReservationLot.objects.filter(space_id=space_id, reserve_date=reserve_date, soft_delete=sentinel_date).exists():
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
        
        # Get the space ID (integer from frontend)
        space_id = validated_data['space']
        
        # Ensure ParkingSpace exists (create minimal space if needed)
        from parking.models import ParkingLot, ParkingSpace
        
        # Get or create a default parking lot
        lot, _ = ParkingLot.objects.get_or_create(
            name='Main Parking Lot',
            defaults={'location': 'Downtown', 'total_spaces': 100}
        )
        
        # Ensure space exists
        ParkingSpace.objects.get_or_create(
            id=space_id,
            defaults={
                'lot': lot,
                'label': f'A{space_id:02d}',
                'is_occupied': False,
                'is_reserved': False,
                'sensor_id': f'sensor_{space_id}'
            }
        )
        
        from datetime import datetime
        from django.utils.timezone import make_aware
        
        # Create reservation using space_id directly (ChatGPT's recommended approach #2)
        return ReservationLot.objects.create(
            user=user, 
            space_id=space_id,  # Pass the ID directly, not the object
            reserve_date=validated_data['reserve_date'],
            ticket_code=ticket_code, 
            soft_delete=make_aware(datetime(1900, 1, 1))
        )
