from importlib.resources import Resource
from multiprocessing.connection import Client

from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    name = models.CharField(max_length=100)
    max_slots = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('queued', 'Queued'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user} - {self.resource} ({self.start_time} - {self.end_time})"
