from django.db import models
from django.contrib.auth.models import User


# Address...
class Address(models.Model):
    country = models.CharField(max_length=20, blank=False)
    state = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    house_number = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.country + ', ' + self.city


# Contact_Details...
class ContactDetails(models.Model):
    phone_number = models.BigIntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.email + ', ' + str(self.phone_number)


# Customers Database...
class Customers(models.Model):

    # Customer Personals...
    customer_name = models.CharField(max_length=200, null=False, unique=True)
    customer_dob = models.DateField()
    customer_aadhaar = models.PositiveIntegerField(blank=False, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    contact_details = models.OneToOneField(ContactDetails, on_delete=models.CASCADE)
    customer_image = models.ImageField(upload_to='Profile Images/', null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.customer_name
