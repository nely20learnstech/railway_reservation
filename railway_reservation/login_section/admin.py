from django.contrib import admin
from .models import CustomUser, City, Itineraries, Schedule, Departure_time, Wagon, TrainSeat, Reservation

# Register your models here.
admin.site.register(CustomUser)

admin.site.register(City)
admin.site.register(Itineraries)
admin.site.register(Schedule)
admin.site.register(Departure_time)
admin.site.register(Wagon)
admin.site.register(TrainSeat)
admin.site.register(Reservation)
