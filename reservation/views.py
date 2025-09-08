from django.shortcuts import render
from .models import ReservationLot
from .models import ParkingSpace
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import ReservationSerializer, ReservationReadSerializer
from django.utils import timezone 
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils.dateparse import parse_date
import logging
from rest_framework.permissions import IsAuthenticated, AllowAny
import pprint

logger = logging.getLogger(__name__)

class ReservationLotView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    def post(self, request):
        reserve_lot = ReservationSerializer(data=request.data, context={'request':request})
        if reserve_lot.is_valid():
            space = reserve_lot.validated_data.get('space')
            reserve_date = reserve_lot.validated_data.get('reserve_date')
            
            try:    
                # lock row
                with transaction.atomic():
                    ReservationLot.objects.select_for_update().filter(space=space)
                    
                    # Check if theres already a reservation
                    exist = ReservationLot.objects.filter(
                        space=space,
                        reserve_date=reserve_date,
                        soft_delete__isnull=True
                    ).exists()
                    
                    logger.warning(f"User{request.user} attempt to double book lot {space.id} for {reserve_date}")
                    
                    if exist:
                        return Response(
                            {"message": "That lot is already reserved at this time"},
                            status=status.HTTP_409_CONFLICT
                        )

                    reserve_lot.save()
                    logger.info(f"User {request.user} reserve lot {space.id} for {reserve_date}")
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

        serialized = ReservationReadSerializer(get_reservation, many=True)
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
        reserve_cancel = get_object_or_404(
            ReservationLot, 
            pk=pk, 
            user=request.user, 
            soft_delete__isnull=True
        )
        
        # soft delete by setting timestamp
        reserve_cancel.soft_delete = timezone.now()
        reserve_cancel.save()
        
        return Response({'message': 'Reservation cancelled successfully'}, status=status.HTTP_200_OK) 


class AvailableView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
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

        # Get reservations for that date to see which spots are taken
        reserved_lots = ReservationLot.objects.filter(
            reserve_date__date=reserve_date,
            soft_delete__isnull=True
        )
        reserved_space_ids = set(reserved_lots.values_list('space_id', flat=True))

        # Dynamically generate available spots (truly unlimited)
        total_spots = 50  # Plenty of spots, can be increased easily
        available_spots = []
        
        for i in range(1, total_spots + 1):
            # Only include spots that aren't reserved on this date
            if i not in reserved_space_ids:
                available_spots.append({
                    'id': i,
                    'label': f'A{i:02d}',
                    'is_occupied': False,
                    'is_reserved': False,
                    'sensor_id': f'sensor_{i}'
                })

        return Response({'available_spots': available_spots}, status=200)
   