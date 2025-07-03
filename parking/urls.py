from django.urls import path
from .views import (
    AvailableParkingSpacesView,
    ParkingLotListView,
    AvailableView  
)

urlpatterns = [
    path('spaces/', AvailableParkingSpacesView.as_view()),
    path('lots/', ParkingLotListView.as_view()),
    path('lots/available/', AvailableView.as_view()),  
]
