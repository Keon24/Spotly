from django.urls import path
from .views import (
    AvailableParkingSpacesView,
    ParkingLotListView,
  
)

urlpatterns = [
    path('spaces/', AvailableParkingSpacesView.as_view()),
    path('lots/', ParkingLotListView.as_view()),
  
]
