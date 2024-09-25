from celery import shared_task
from .models import Booking
from django.utils import timezone

@shared_task
def check_bookings():
    now = timezone.now()
    expired_bookings = Booking.objects.filter(status='active', end_time__lt=now)

    for booking in expired_bookings:
        booking.status = 'completed'
        booking.save()

    print(f"Updated {expired_bookings.count()} expired bookings to 'completed'.")
