from django.db import models
from customers.models import Customers


# Classification of Rooms...
class RoomType(models.Model):
    type = models.CharField(max_length=30, unique=True)
    room_price = models.IntegerField()

    def __str__(self):
        return self.type


# Floors...
class Floor(models.Model):
    floor = models.PositiveIntegerField(blank=False, unique=True)

    def __str__(self):
        return str(self.floor)


# Blocks...
class BlockFloor(models.Model):
    block = models.CharField(max_length=2, blank=False)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)

    def __str__(self):
        return self.block + ' block, ' + str(self.floor.floor) + ' floor'


# Rooms Database...
class Room(models.Model):
    block_floor = models.ForeignKey(BlockFloor, on_delete=models.PROTECT)

    room_number = models.PositiveIntegerField(blank=False)
    room_type_price = models.ForeignKey(RoomType, on_delete=models.PROTECT)

    booked_customer = models.ForeignKey(Customers, on_delete=models.PROTECT, null=True, blank=True)

    booked_time = models.DateTimeField(default=None, null=True, blank=True)
    booked_days = models.IntegerField(default=0, null=True, blank=True)
    deadline = models.DateTimeField(default=None,null=True, blank=True)

    def __str__(self):
        if self.booked_customer is None:
            return self.block_floor.block + ', ' +\
                   str(self.block_floor.floor) + ', ' + str(self.room_number) + ', '\
                   + self.room_type_price.type + ', ' + str(self.room_type_price.room_price)
        else:
            return str(self.block_floor.block) + ', ' + str(self.block_floor.floor) + ', ' + str(self.room_number) + \
                   ', '+ self.room_type_price.type + ', ' + str(self.room_type_price.room_price) + \
                   ' ( Booked by ' + self.booked_customer.customer_name + ' )'
