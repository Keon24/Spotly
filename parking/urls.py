from django.urls import path
from .views import (
    AvailableParkingSpacesView,
    ParkingLotListView,
    setup_parking_spaces,
)

urlpatterns = [
    path('spaces/', AvailableParkingSpacesView.as_view()),
    path('lots/', ParkingLotListView.as_view()),
    path('setup/', setup_parking_spaces, name='setup-parking-spaces'),
]
