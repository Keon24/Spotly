from django.shortcuts import render
from .models import ReservationLot
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import ReservationSerializer
from django.utils import timezone 


class ReservationLotView(APIView):
    def post(self,request):
        reserve_lot = ReservationSerializer(data=request.data)
        if reserve_lot.is_valid():
            reserve_lot.save()
            return Response(
                {'Message:',"Parking Reservation Confirmed","data", reserve_lot.data},
                status=status.HTTP_201_CREATED
            )
        else: return Response({'message:','Reservation Failed',"data", reserve_lot.data},
                status=status.HTTP_404_NOT_FOUND)
        
        
class ReservationDateView(APIView):
     def get (self,request):
         now = timezone.now()
         reserve_date = ReservationSerializer(ReservationLot.objects.filter(user=request.user, reserved_for__gt=now,many=True))
         return reserve_date.data
         
        
