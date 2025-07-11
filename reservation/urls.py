from django.urls import path 
from .views import ReservationLotView, ReservationDeleteView, ReservationDateView,AvailableView

urlpatterns = [
  path('', ReservationLotView.as_view()),  # handles GET/POST for reservations
  path('<int:pk>/cancel/', ReservationDeleteView.as_view()),
  path('dates/', ReservationDateView.as_view()),  
  path('available/', AvailableView.as_view()),
]
