import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from RoomService.models import *
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from customers.models import *
from django.contrib import messages
import threading
import time

# Counting total number of Customers...
number_of_customers = len(Customers.objects.all())
# .....................................

# Counting total number of Employees...
number_of_employees = len(RoomsManagingEmployees.objects.all())
# .....................................

# Counting total number of blocks...
number_of_blocks = 0
blocks = []

for block in BlockFloor.objects.values_list('block'):
    if block not in blocks:
        blocks.append(block)
        number_of_blocks += 1
    else:
        pass
# .....................................

# Counting total number of rooms...
number_of_rooms = len(Room.objects.all())

# .....................................

# Counting total types of rooms...
room_type_price = []
for room_type in RoomType.objects.all():
    room_type_price.append((room_type.type, room_type.room_price))


# .....................................
args = {'customers_count': number_of_customers, 'blocks_count': number_of_blocks, 'rooms_count': number_of_rooms,
        'employees_count': number_of_employees, 'room_type_price': room_type_price}


# Landing Page...

def landing_page(request):
    return render(request, 'room_management/landing_page.html', args)


def home(request):
    username = request.user.username
    args['username'] = username
    return render(request, 'room_management/home.html', args)


# Manager Registration...
def add_customer(request):
    if request.method == 'POST':
        # Customer Details...
        cust_aadhaar = request.POST['aadhaar']
        if not Customers.objects.filter(customer_aadhaar=cust_aadhaar):
            cust_name = request.POST['cust_name']
            cust_dob = request.POST['cust_dob']
            cust_gender = request.POST['gender']

            # Address...
            cust_country = request.POST['country']
            cust_city = request.POST['city']
            cust_state = request.POST['state']
            cust_house_number = request.POST['house_number']

            addr = Address.objects.create(country=cust_country, state=cust_state, city=cust_city, house_number=cust_house_number)
            addr.save()

            # ........................................

            # Contact Details...
            cust_email = request.POST['email']
            cust_phone_number = request.POST['phn_number']

            cntct = ContactDetails.objects.create(email=cust_email, phone_number=cust_phone_number)
            cntct.save()

            # ........................................

            try:
                cust_image = request.FILES['image']
            except:
                cust_image = None

            customer_details = Customers.objects.create(customer_aadhaar=cust_aadhaar, customer_name=cust_name,
                                                        customer_dob=cust_dob, address=addr, contact_details=cntct,
                                                        gender=cust_gender, customer_image=cust_image)
            customer_details.save()

            messages.success(request, 'Customer added successfully.')

            return redirect('room_management:home')

        else:
            messages.error(request, 'Customer Already Exists!!')

        return redirect('room_management:add-customer')

    else:
        return render(request, 'room_management/add_customer.html')


def edit_customer_details(request, customer_aadhaar):

    if request.method == 'POST':
        customer = Customers.objects.get(customer_aadhaar=customer_aadhaar)

        customer.customer_name = request.POST['cust_name']
        try:
            customer.customer_image = request.FILES['image']
        except:
            pass

        contact_details = ContactDetails.objects.get(phone_number=customer.contact_details.phone_number,
                                                     email=customer.contact_details.email)
        contact_details.phone_number = request.POST['phn_number']
        contact_details.email = request.POST['email']
        contact_details.save()

        customer.contact_details = contact_details

        customer.save()

    else:
        pass

    return redirect('room_management:customer-profile', customer_aadhaar)


def delete_customer(request, customer_aadhaar):
    customer = Customers.objects.get(customer_aadhaar=customer_aadhaar)
    address = Address.objects.get(country=customer.address.country, city=customer.address.city,
                                  state=customer.address.state, house_number=customer.address.house_number)
    contact_details = ContactDetails.objects.get(email=customer.contact_details.email,
                                                 phone_number=customer.contact_details.phone_number)

    customer.delete()
    address.delete()
    contact_details.delete()

    return redirect('room_management:customers-list')


# Room Management Login...
def room_manager_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            return redirect('room_management:home')

        else:
            messages.error(request, 'Invalid Login details')

        return redirect('room_management:login')

    else:
        return render(request, 'room_management/login.html')


# Logout...
def room_manager_logout(request):
    logout(request)
    return redirect('room_management:landing-page')


# Customers.............................................................................................................
def customers_list(request):
    customers = Customers.objects.all()
    customers = {'customers': customers}

    return render(request, 'customers/customers.html', customers)


def customer_profile(request, customer_aadhaar):
    customer_details = Customers.objects.get(customer_aadhaar=customer_aadhaar)
    customer = {'customer_details': customer_details}

    return render(request, 'room_management/profile.html', customer)


threads = []
# Booking A Room...
def book_room(request):

    request.session.set_expiry(240)
    empty_rooms = []
    for room in Room.objects.all():
        if room.booked_customer == None:
            empty_rooms.append(room)

    room_args = {'empty_rooms': empty_rooms, 'customers': Customers.objects.all()}

    if request.method == 'POST':
        selected_room = request.POST['room']

        selected_room = tuple(selected_room.split(','))

        floor = Floor.objects.get(floor=selected_room[1])
        block_floor = BlockFloor.objects.get(floor=floor, block=selected_room[0])
        room = Room.objects.get(block_floor=block_floor, room_number=selected_room[2])

        customer = Customers.objects.get(customer_aadhaar=request.POST['aadhaar'])
        booked_days = request.POST['days']

        deadline = datetime.datetime.now() + timedelta(days=int(booked_days))

        room.booked_customer = customer
        room.booked_time = datetime.datetime.now()
        room.booked_days = booked_days
        room.deadline = deadline

        room.save()

        thread = threading.Thread(target=unbook_room, args=(room,))
        thread.start()
        threads.append((thread, room))

        return redirect('room_management:home')

    return render(request, 'room_management/book_room.html', room_args)


def unbook_room(curr_room):
    time.sleep(int(curr_room.booked_days)*24*60*60)
    curr_room.booked_customer = None
    curr_room.booked_time = None
    curr_room.booked_days = None

    curr_room.save()
    for thread, room in threads:
        if room == curr_room:
            thread.join()
            break

    return redirect('room_management:booked_rooms')

def booked_room(request):
    booked_rooms = []
    for room in Room.objects.all():
        if room.booked_customer != None:
            booked_rooms.append(room)

    return render(request, 'room_management/booked_rooms.html',{'rooms':booked_rooms})