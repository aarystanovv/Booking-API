from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Resource, Booking
from .serializer import ResourceSerializer, BookingSerializer
from django.db.models import Q
from datetime import datetime
from .tasks import check_bookings

@api_view(['GET', 'POST'])
def resource_list(request):
    if request.method == 'GET':
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        check_bookings.delay()
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        check_bookings.delay()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        resource = serializer.validated_data['resource']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        conflicting_bookings = Booking.objects.filter(
            resource=resource,
            status='active',
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if conflicting_bookings.exists():
            serializer.save(status='queued')
            return Response({'message': 'All slots are taken, added to queue.'}, status=status.HTTP_202_ACCEPTED)
        else:
            serializer.save(status='active')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    check_bookings.delay()

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if booking.status == 'active':
            booking.status = 'completed'
            booking.save()
            next_booking = Booking.objects.filter(resource=booking.resource, status='queued').first()
            if next_booking:
                next_booking.status = 'active'
                next_booking.save()
                print(f"Notification: Slot is now available for {next_booking.user}")
            return Response({'message': 'Booking cancelled and next user notified.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Booking is not active.'}, status=status.HTTP_400_BAD_REQUEST)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def booking_list(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    check_bookings.delay()
    return Response(serializer.data)
