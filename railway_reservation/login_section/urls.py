from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('custom-admin/', views.custom_admin, name='custom-admin'),
    path('signup', views.register_view, name="signup"),
    path('signin', views.login_view, name="signin"),
    path('signout', views.logout_view, name="signout"),
    path('reservation', views.reservation, name="reservation"),
    path('city-json/', views.get_json_city_data, name="city-json"),
    path('itinerary-json/<str:city>/', views.get_json_itinerary_data, name="itinerary-json"),
    path('fee-json/<str:departure>/<str:arrival>/', views.get_json_fee_data, name="fee-json"),
    path('add-reservation', views.add_reservation, name="add-reservation"),
    path('individual_reservation/<str:reservation_id>', views.individual_reservation, name="individual_reservation"),
    path('edit-reservation', views.edit_reservation, name="edit-reservation"),
    path('delete-reservation/<int:reservation_id>', views.delete_reservation, name="delete-reservation"),
    path('further-details/<int:reservation_id>', views.further_details, name="further-details"),

     path('ticket/', views.generate_ticket, name='generate_ticket'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
