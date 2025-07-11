from rest_framework import serializers
from .models import ReservationLot
import uuid

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationLot
        fields = ['space', 'reserve_date']  # correct field names
        read_only_fields = ['ticket_code', 'user' 'created_at']

    def validate(self, attrs):
        space = attrs.get('space')
        reserve_date = attrs.get('reserve_date')

        if ReservationLot.objects.filter(space=space, reserve_date=reserve_date, soft_delete__isnull=True).exists():
            raise serializers.ValidationError("This space is already reserved at that time.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        ticket_code = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        return ReservationLot.objects.create(user=user, ticket_code=ticket_code, **validated_data)
