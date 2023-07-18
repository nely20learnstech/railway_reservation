from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=False)

class City(models.Model):
    city_name = models.CharField(max_length=80)

    def __str__(self):
        return str(self.city_name)


class Itineraries(models.Model):
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures')
    arrival_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrivals')
    adult_fee = models.IntegerField()
    child_fee = models.IntegerField()
    duration = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.departure_city} - {self.arrival_city}"
    

class Schedule(models.Model):
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures_fee')
    arrival_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrivals_fee')
    departure_time = models.TimeField()

    def __str__(self):
        return f"{self.departure_city} - {self.arrival_city}"
    
class Departure_time(models.Model):
    departure_time = models.TimeField()

class Wagon(models.Model):
    wagon = models.CharField(max_length=50)

class TrainSeat(models.Model):
    seat_number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)
    

class SecondWagon(models.Model):
    seat_number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)

class ThirdWagon(models.Model):
    seat_number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)


class Reservation(models.Model):
    reservation_id = models.IntegerField(primary_key=True)
    departure_city = models.CharField(max_length=80)
    destination_city = models.CharField(max_length=80)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    traveler_name = models.CharField(max_length=200)
    child_number = models.IntegerField(default=0)
    adult_number = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15)
    chosen_class = models.CharField(max_length=50)
    seat_number_list = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    

    def __int__(self):
        return self.reservation_id
    
    def __str__(self):
        return self.traveler_name
    
    
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(f'{self.reservation_id}-{self.traveler_name}')
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        file_name = f'qr_code-{self.reservation_id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        # Don't change to True, an infinite loop will occur. 
        self.qr_code.save(file_name, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)