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
    class Meta:
        model = ReservationLot
        fields = ['space', 'reserve_date']
        read_only_fields = ['ticket_code', 'user', 'created_at']

    def validate(self, attrs):
        space = attrs.get('space')
        reserve_date = attrs.get('reserve_date')
        user = self.context['request'].user

        # Check if space is already reserved at this exact time
        if ReservationLot.objects.filter(space=space, reserve_date=reserve_date, soft_delete__isnull=True).exists():
            raise serializers.ValidationError("This space is already reserved at that exact time.")

        # Check if user already has a reservation for this date (ignoring time)
        if ReservationLot.objects.filter(
            user=user, 
            reserve_date__date=reserve_date.date(), 
            soft_delete__isnull=True
        ).exists():
            raise serializers.ValidationError("You already have a reservation for this date. Only one reservation per day is allowed.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        ticket_code = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        return ReservationLot.objects.create(user=user, ticket_code=ticket_code, **validated_data)
