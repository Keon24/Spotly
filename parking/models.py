from django.db import models

# ParkingLot
class ParkingLot(models.Model):
# - name: Name of the parking lot 
    name = models.CharField(max_length=100)
# - location: Street address or GPS coordinates
    location = models.CharField(max_length=255)
# - total_spaces: How many total spots exist 
    total_spaces = models.IntegerField(null=True, blank= True)
# - created_at: Timestamp when the lot was added 
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.CharField(max_length=50, default='')
    
    def _str_(self):
        return self.name
    
    def parking_access(self):
        return self.spaces.filter(is_occupied=False).count
    

# ParkingSpace
class ParkingSpace(models.Model):
    lot = models.ForeignKey(ParkingLot,on_delete=models.CASCADE, related_name='spaces')
#  label: Spot label or number 
    label = models.CharField(max_length=255)
#  is_occupied: Boolean indicating if the spot is currently taken
    is_occupied = models.BooleanField(default= False)
#  is_reserved: 
    is_reserved = models.BooleanField(default= False)
    sensor_id = models.CharField(max_length= 100)

