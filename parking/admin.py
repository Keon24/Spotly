from django.contrib import admin
from .models import ParkingLot,ParkingSpace
# Register your models here.
@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','location','total_spaces','created_at']
    
@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
     list_display = ('id', 'lot', 'label', 'is_occupied', 'is_reserved', 'sensor_id')    