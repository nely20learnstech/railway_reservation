from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .models import City, Itineraries, Departure_time, Wagon, TrainSeat, Reservation, ThirdWagon, SecondWagon #, Schedule
from django.utils.translation import activate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO


# Create your views here.
def home(request):
    return render(request, "login_section/index.html")

def login_view(request):
    activate('fr')
    queryset = City.objects.all()
    departure_time = Departure_time.objects.all()
    seat_numbers = ThirdWagon.objects.all()
    wagons = Wagon.objects.all()
    reservations = Reservation.objects.all().order_by('-created_at')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            name = user.username
            context = {
                'departure_time': departure_time,
                'queryset': queryset,
                'seat_numbers': seat_numbers,
                'wagons': wagons,
                'reservations': reservations,
                'name': name
            }

            if user.is_superuser:
                return render(request, "login_section/custom-admin.html", context)

            return render(request, "login_section/user.html", context)
        else:
            messages.error(request, "Votre email ou mot de passe n'est pas correct!")
            return redirect('home')
        
    return render(request, "login_section/user.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')


def register_view(request):
    activate('fr')
    queryset = City.objects.all()
    departure_time = Departure_time.objects.all()
    seat_numbers = TrainSeat.objects.all()
    wagons = Wagon.objects.all()
    reservations = Reservation.objects.all().order_by('-created_at')
    if request.method == 'POST':
            username = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['password']
            # password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                # form.add_error('confirm_password', 'Passwords do not match')
                return render(request, 'login_section/index.html', {'form': 'Passwords do not match'})
            else:           
            
                user = CustomUser.objects.create(email=email, username=username)
                # user = form.save(commit=False)
                user.set_password(password)
                user.save()

                # Log in the user
                user = authenticate(request, email=user.email, password=password)
                if user is not None:
                    login(request, user)
                    context = {
                        'departure_time': departure_time,
                        'queryset': queryset,
                        'seat_numbers': seat_numbers,
                        'wagons': wagons,
                        'reservations': reservations,
                        'name': username
                    }
                    # Redirect to the desired page
                    return render(request, 'login_section/user.html', context)        

    return render(request, 'login_section/index.html')



# Create your views here.
def reservation(request):
    activate('fr')
    wagon2_seat_numbers = SecondWagon.objects.all()
    wagon3_seat_numbers = ThirdWagon.objects.all()
    queryset = City.objects.all()
    departure_time = Departure_time.objects.all()
    seat_numbers = TrainSeat.objects.all()
    wagons = Wagon.objects.all()
    reservations = Reservation.objects.all().order_by('-created_at')
  
    available_list = []
    taken_list = []

    if request.method == 'POST':
        if request.POST['seat_number_checkbox']:
                seat_number_list = request.POST.getlist('seat_number_checkbox')
                if seat_number_list is None:
                   return render(request, 'login_section/user.html', {'error': 'Please enter a seat number.'})  
        else:
            return render(request, 'login_section/user.html', {'error': 'Please enter a seat number.'})
        
        try:

            for x in seat_number_list:
                # Get and check seat one by one  
                seat = TrainSeat.objects.get(seat_number = int(x))
                if seat.is_available:
                    available_list.append(seat.seat_number)
                    TrainSeat.objects.filter(seat_number=int(x)).update(is_available=False)
                else:
                    # Seat is already taken, handle accordingly
                    taken_list.append(seat.seat_number)


            if len(taken_list) > 0 and len(available_list) > 0: 
                return render(request, 'login_section/user.html', {'success': f'Thank you for choosing a seat! Seat Number: {available_list}. \
                                                                             But, Seat number {taken_list}  is already taken. Please choose other {len(taken_list)} place(s) to complete the count.'})           
            if len(available_list) > 0:
                return render(request, 'login_section/user.html', {'success': f'Thank you for choosing a seat! Seat Number: {available_list}.'})    
            if len(taken_list) > 0:
                return render(request, 'login_section/user.html', {'error': f'Seat number {taken_list}  is already taken.'})  
        except TrainSeat.DoesNotExist:
                # Invalid seat number, handle accordingly
                return render(request, 'login_section/user.html', {'error': 'Invalid seat number.'})
        
   

    context = {
        'departure_time': departure_time,
        'queryset': queryset,
        'seat_numbers': seat_numbers,
        'wagon3_seat_numbers': wagon3_seat_numbers,
        'wagon2_seat_numbers': wagon2_seat_numbers,
        'wagons': wagons,
        'reservations': reservations,
    }

    return render(request, 'login_section/user.html', context)

def get_json_city_data(request):
    queryset_value = list(City.objects.values())
    return JsonResponse({'data': queryset_value})

def get_json_itinerary_data(request, *args, **kwargs):
    selected_city = kwargs.get('city')
    obj_itinerary = list(Itineraries.objects.filter(departure_city__city_name=selected_city).values('arrival_city__city_name'))
    # return render(request, 'itinerary/main.html', {'itinerary': selected_city})
    print(len(obj_itinerary))
    print(selected_city)
    return JsonResponse({'data': obj_itinerary})

def get_json_fee_data(request, *args, **kwargs):
    selected_departure_city = kwargs.get('departure')
    selected_arrival_city = kwargs.get('arrival')
    obj_fee = list(Itineraries.objects.filter(departure_city__city_name=selected_departure_city, arrival_city__city_name=selected_arrival_city).values())
    print(len(obj_fee))
    print(selected_arrival_city)
    print(selected_departure_city)
    return JsonResponse({'data': obj_fee})

# Add reservation
def add_reservation(request):
    available_list = []
    taken_list = []
    if request.method == 'POST':
        if request.POST.get('departure_city')\
            and request.POST.get('destination_city') \
            and request.POST.get('departure_date') \
            and request.POST.get('departure_time') \
            and request.POST.get('traveler_name') \
            or request.POST.get('child_number') \
            or request.POST.get('adult_number') \
            and request.POST.get('phone_number') \
            and request.POST.get('chosen_class') \
            and request.POST.get('seat_number_checkbox'):
            # Saving a reservation instance
            reservation = Reservation()
            reservation.departure_city = request.POST.get('departure_city')
            reservation.destination_city = request.POST.get('destination_city')
            reservation.departure_date = request.POST.get('departure_date')
            reservation.departure_time = request.POST.get('departure_time')
            reservation.traveler_name = request.POST.get('traveler_name')
            reservation.child_number = request.POST.get('child_number')
            if reservation.child_number =='':
                reservation.child_number = 0
            reservation.adult_number = request.POST.get('adult_number')
            if reservation.adult_number =='':
                reservation.adult_number = 0       
            reservation.phone_number = request.POST.get('phone_number')
            reservation.chosen_class = request.POST.get('chosen_class')
            reservation_list = request.POST.getlist('seat_number_checkbox')
            reservation.seat_number_list = ', '.join(reservation_list)
            reservation.save()

            if request.method == 'POST':
                if request.POST['seat_number_checkbox']:
                        seat_number_list = request.POST.getlist('seat_number_checkbox')
                        if seat_number_list is None:
                            return render(request, 'login_section/user.html', {'error': 'Please enter a seat number.'})  
                else:
                    return render(request, 'login_section/user.html', {'error': 'Please enter a seat number.'})
                
                try:

                    for x in seat_number_list:
                        # Get and check seat one by one  
                        seat = TrainSeat.objects.get(seat_number = int(x))
                        if seat.is_available:
                            available_list.append(seat.seat_number)
                            TrainSeat.objects.filter(seat_number=int(x)).update(is_available=False)
                        else:
                            # Seat is already taken, handle accordingly
                            taken_list.append(seat.seat_number)


                    if len(taken_list) > 0 and len(available_list) > 0: 
                        return render(request, 'itinerary/main.html', {'success': f'Thank you for choosing a seat! Seat Number: {available_list}. \
                                                                             But, Seat number {taken_list}  is already taken. Please choose other {len(taken_list)} place(s) to complete the count.'})           
                    if len(available_list) > 0:
                        return render(request, 'itinerary/main.html', {'success': f'Thank you for choosing a seat! Seat Number: {available_list}.'})    
                    if len(taken_list) > 0:
                        return render(request, 'itinerary/main.html', {'error': f'Seat number {taken_list}  is already taken.'})  
                except TrainSeat.DoesNotExist:
                        # Invalid seat number, handle accordingly
                        return render(request, 'login_section/user.html', {'error': 'Invalid seat number.'})
        
            return HttpResponseRedirect('reservation')
    

# Edit reservation
def edit_reservation(request):
    available_list = []
    taken_list = []
    if request.method == 'POST':
        reservation = Reservation.objects.get(reservation_id = request.POST.get('reservation_id'))
        if reservation != None:
            reservation.departure_city = request.POST.get('departure_city')
            reservation.destination_city = request.POST.get('destination_city')
            reservation.departure_date = request.POST.get('departure_date')
            reservation.departure_time = request.POST.get('departure_time')
            reservation.traveler_name = request.POST.get('traveler_name')
            reservation.child_number = request.POST.get('child_number')
            if reservation.child_number == '':
                reservation.child_number = 0 
            reservation.adult_number = request.POST.get('adult_number')    
            if reservation.adult_number == '':
                reservation.adult_number = 0 
            reservation.phone_number = request.POST.get('phone_number')
            reservation.chosen_class = request.POST.get('chosen_class')
            # reservation.seat_number_list = request.POST.getlist('seat_number_checkbox')
            reservation_list = request.POST.getlist('seat_number_checkbox')
            reservation.seat_number_list = ', '.join(reservation_list)
            reservation.save()

            if request.method == 'POST':
                if request.POST['seat_number_checkbox']:
                        seat_number_list = request.POST.getlist('seat_number_checkbox')
                        if seat_number_list is None:
                            return render(request, 'login_section/user.html', {'error': 'Please enter a seat number.'})  
                else:
                    return render(request, 'login_section/user.html', {'error': 'Please enter a seat number.'})
                
                try:

                    for x in seat_number_list:
                        # Get and check seat one by one  
                        seat = TrainSeat.objects.get(seat_number = int(x))
                        if seat.is_available:
                            available_list.append(seat.seat_number)
                            TrainSeat.objects.filter(seat_number=int(x)).update(is_available=False)
                        else:
                            # Seat is already taken, handle accordingly
                            taken_list.append(seat.seat_number)


                    if len(taken_list) > 0 and len(available_list) > 0: 
                        return render(request, 'itinerary/main.html', {'success': f'Thank you for choosing a seat! Seat Number: {available_list}. \
                                                                             But, Seat number {taken_list}  is already taken. Please choose other {len(taken_list)} place(s) to complete the count.'})           
                    if len(available_list) > 0:
                        return render(request, 'itinerary/main.html', {'success': f'Thank you for choosing a seat! Seat Number: {available_list}.'})    
                    if len(taken_list) > 0:
                        return render(request, 'itinerary/main.html', {'error': f'Seat number {taken_list}  is already taken.'})  
                except TrainSeat.DoesNotExist:
                        # Invalid seat number, handle accordingly
                        return render(request, 'login_section/user.html', {'error': 'Invalid seat number.'})
        
            # return HttpResponseRedirect('reservation')
            return HttpResponseRedirect('reservation')
        

# Delete reservation
def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(reservation_id = reservation_id)
    reservation.delete()
    return HttpResponseRedirect('/reservation')
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# View the reservation individually
def individual_reservation(request, reservation_id):
    activate('fr')
    reservation = Reservation.objects.get(reservation_id = reservation_id)
    if reservation is not None:
        return render(request, "login_section/edit.html", {'reservation': reservation})

# @user_passes_test(lambda user: user.is_superuser) 
// Admin only can access the page.
@staff_member_required   
def custom_admin(request):
    activate('fr')
    reservations = Reservation.objects.all()
    return render(request, "login_section/custom-admin.html", {'reservations': reservations})

def further_details(request, reservation_id):
    activate('fr')
    reservation = Reservation.objects.get(reservation_id = reservation_id)
    departure = reservation.departure_city
    destination = reservation.destination_city
    number_of_adult = reservation.adult_number
    number_of_children = reservation.child_number
     # Get departure and arrival city from reservation
    adult_fee_query = Itineraries.objects.filter(departure_city__city_name = departure, arrival_city__city_name=destination).values('adult_fee')
    child_fee_query = Itineraries.objects.filter(departure_city__city_name = departure, arrival_city__city_name=destination).values('child_fee')
    adult_fee = adult_fee_query.first()['adult_fee']
    child_fee = child_fee_query.first()['child_fee']
    total = int(number_of_adult) * int(adult_fee) +  int(number_of_children) * int(child_fee)
    print(adult_fee)
    print(reservation)
    context = {
        'total' : total,
        'reservation': reservation,
    }
    return render(request, "login_section/further-details.html", context)
