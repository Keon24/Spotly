from django.urls import path 
from .views import ReservationLotView, ReservationDeleteView

urlpatterns = [
  path('', ReservationLotView.as_view()),  # handles GET/POST for reservations
    path('<int:pk>/cancel/', ReservationDeleteView.as_view()),
]
