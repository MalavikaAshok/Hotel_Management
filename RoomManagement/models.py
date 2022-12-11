from django.db import models
from django.contrib.auth.models import User


# Room Management Employees...
class RoomsManagingEmployees(models.Model):
    employee_user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10)
    employee_dob = models.DateField()

    def __str__(self):
        return self.employee_id + ',' + self.employee_user.username