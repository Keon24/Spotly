from django.shortcuts import render
from .models import ReservationLot
from .models import ParkingSpace
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import ReservationSerializer
from django.utils import timezone 
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils.dateparse import parse_date
import logging
from rest_framework.permissions import IsAuthenticated
import pprint

logger = logging.getLogger(__name__)

class ReservationLotView(APIView):
    def post(self, request):
        reserve_lot = ReservationSerializer(data=request.data)
        if reserve_lot.is_valid():
            lot = reserve_lot.validated_data.get('lot')
            reserve_date = reserve_lot.validated_data.get('reserve_date')
            
            try:    
                # lock row
                with transaction.atomic():
                    ReservationLot.objects.select_for_update().filter(lot=lot)
                    
                    # Check if theres already a reservation
                    exist = ReservationLot.objects.filter(
                        lot=lot,
                        reserve_date=reserve_date,
                        soft_delete__isnull=True
                    ).exists()
                    
                    logger.warning(f"User{request.user} attempt to double book lot {lot.id} for {reserve_date}")
                    
                    if exist:
                        return Response(
                            {"message": "That lot is already reserved at this time"},
                            status=status.HTTP_409_CONFLICT
                        )

                    reserve_lot.save(user=request.user)
                    logger.info(f"User {request.user} reserve lot {lot.id} for {reserve_date}")
                    return Response(
                        {
                            "Message": "Parking Reservation Confirmed",
                            "data": reserve_lot.data
                        },
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                logging.error(f'Reservation failed for user{request.user}:{str(e)}')
                logger.warning(f"Invalid reservation by user{request.user}:{reserve_lot.errors}")
                return Response(
                    {'message': 'Reservation Failed', "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {'message': 'Reservation Failed', "data": reserve_lot.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
                
        
    def get(self, request):
        now = timezone.now()
        # Admin sees all reservations
        if request.user.is_admin:
            get_reservation = ReservationLot.objects.all()
        else:    
            # Regular users see only their upcoming, active reservations
            get_reservation = ReservationLot.objects.filter(
                user=request.user, 
                reserve_date__gt=now,
                soft_delete__isnull=True
            )

        serialized = ReservationSerializer(get_reservation, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    
class ReservationDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("HEADERS RECEIVED:")
        pprint.pprint(dict(request.headers))

        now = timezone.now()
        reserve_date = ReservationSerializer(
            ReservationLot.objects.filter(
                user=request.user,
                reserve_date__gte=now
            ),
            many=True
        )
        return Response(reserve_date.data, status=status.HTTP_200_OK)

class ReservationDeleteView(APIView):
    def post(self, request, pk):
        reserve_cancel = get_object_or_404(ReservationLot, pk=pk)
        
        if not reserve_cancel.is_active:
            return Response({'message': 'Reservation is already canceled'}, status=status.HTTP_404_NOT_FOUND)

        # soft delete 
        reserve_cancel.is_active = False 
        reserve_cancel.save()
        
        return Response({'message': 'Reservation Approved'}, status=status.HTTP_200_OK) 


class AvailableView(APIView):
    def get(self, request):
        # Get the date from query parameters (?date=YYYY-MM-DD)
        date_str = request.GET.get('date')
        # If it's missing, return a 400 error
        if not date_str:
            return Response({'message': 'missing date'}, status=400)

        # Parse the date string into a datetime.date object
        reserve_date = parse_date(date_str)
        # If parsing fails, return a 400 error for invalid format
        if not reserve_date:
            return Response({"error": "Invalid date format"}, status=400)

        # Query ReservationLot for reservations on that date
        # Only include reservations that are not soft-deleted
        # Extract the lot IDs from these reservations
        reserved_lots = ReservationLot.objects.filter(
            reserve_date=reserve_date,
            soft_delete__isnull=True
        )    
        reserve_ids = reserved_lots.values_list('space_id', flat=True)

        # Query Parkingspace (or your lot model) for available spots
        # Filter: is_occupied == False
        # Exclude any lot IDs that are in the reserved list
        available_spots = ParkingSpace.objects.filter(is_occupied=False).exclude(id__in=reserve_ids)

        if not available_spots.exists():
            # Format the response data with the lot info you want to return
            return Response({'message': 'reservation occupied choose another a date'}, status=400)

        # Return the available lots with a 200 OK response
        return Response({'available_spots': list(available_spots.values())}, status=200)
