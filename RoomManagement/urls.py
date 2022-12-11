from django.urls import path
from .views import *


app_name = 'room_management'

urlpatterns = [

    path('', landing_page, name='landing-page'),
    path('home/', home, name='home'),
    path('customer/', add_customer, name='add-customer'),
    path('login/', room_manager_login, name='login'),
    path('logout/', room_manager_logout, name='logout'),

    path('customers/', customers_list, name='customers-list'),
    path('customers/<customer_aadhaar>/', customer_profile, name='customer-profile'),
    path('customers/<customer_aadhaar>/edit_customer/', edit_customer_details, name='edit-details'),
    path('customers/<customer_aadhaar>/delete_customer/', delete_customer, name='delete-customer'),

    path('book_room/', book_room, name='book-room'),
    path('booked_rooms',booked_room, name='booked_rooms'),

]
