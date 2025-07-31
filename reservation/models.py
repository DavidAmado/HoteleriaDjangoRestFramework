from django.db import models

# Create your models here.
class Guest(models.Model):
    nombre = models.CharField()
    correo = models.EmailField()
    telefono = models.CharField(blank=True)

class Room(models.Model):
    numero = models.CharField(primary_key=True)

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
    status = models.CharField(default='pending')
