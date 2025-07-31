from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from reservation.models import Guest, Room, Reservation
from reservation.serializers import GuestSerializer, RoomSerializer, ReservationDictSerializer, ReservationIDSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone

# Create your views here.

class ReservationViewSet(viewsets.ViewSet):
    queryset = Reservation.objects.all()
    def create(self, request):
        guest = request.data.get('guest')
        print ("request", request)
        print ("request.data", request.data)
        print ("asd", guest)
        if isinstance(guest, dict):
            serializer = ReservationDictSerializer(data=request.data)
        else:
            serializer = ReservationIDSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Reservation.objects.all()
        serializer = ReservationDictSerializer(queryset, many=True)
        return Response(serializer.data)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ReservationCheckIn(APIView):
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            raise ValueError("reservation ID no encontrado")
        try:
            other_reservation = Reservation.objects.get(room=reservation.room, status='inhouse')
        except Reservation.DoesNotExist:
            other_reservation = False
        message = "Checked in satisfactorio."
        if other_reservation:
            other_reservation.status='cancelled'
            other_reservation.save()
            message = message + " Se cancelo otra reserva."
        reservation.status = 'inhouse'
        reservation.check_in = timezone.now()
        reservation.save()
        
        return Response({"message": message}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class ReservationCheckOut(APIView):
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            raise ValueError("reservation ID no encontrado")
        if reservation.status == 'inhouse':
            reservation.status = 'completed'
            reservation.check_out = timezone.now()
            reservation.save()
            return Response({"message": "Checked out satisfactorio"}, status=status.HTTP_200_OK)
        return Response({"message": "Checked out no es posible puesto que no ha hecho check in"}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class IsRoomsAviable(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise ValueError("Room ID no encontrado")
        try:
            reservation = Reservation.objects.get(room=room_id, status='inhouse')
        except Reservation.DoesNotExist:
            reservation = None

        if reservation:
            return Response({"message": "ocupada"}, status=status.HTTP_200_OK)
        return Response({"message": "disponible"}, status=status.HTTP_200_OK)