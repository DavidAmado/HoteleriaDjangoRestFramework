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

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    def get_serializer_class(self):
        """
        De esta manera se elige serializer, dependeindo del dato que viene para poder, con la misma url 
        responder 2 payloads distintos sin que falle por comprobacion de campos.
        """
        guest = self.request.data.get('guest')
        if isinstance(guest, dict):
            return ReservationDictSerializer
        else:
            return ReservationIDSerializer

    def list(self, request):
        """
        declaro el metodo list para que liste con el serializer completo
        """
        queryset = Reservation.objects.all()
        serializer = ReservationDictSerializer(queryset, many=True)
        return Response(serializer.data)
    def update(self, request, pk):
        """
        declaro el metodo update para que actualize con el serializer completo
        """
        instance = self.get_object()
        serializer = ReservationIDSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ReservationCheckIn(APIView):
    """
    view encargada de hacer checkin guardar hora, y validar si existe otra reserva solapada
    """
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
    """
    view encargada de hacer chekout y guardar la hora
    """
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
class ReservationCancelled(APIView):
    """
    view encargada de hacer cancelar reserva
    """
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            raise ValueError("reservation ID no encontrado")
        if reservation.status == 'pending':
            reservation.status = 'cancancelled'
            reservation.save()
            return Response({"message": "reserva cancelada satisfactoriamente"}, status=status.HTTP_200_OK)
        return Response({"message": "cancelar no es posible puesto que el estado actual es "+reservation.status}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class IsRoomsAviable(APIView):
    """
    view encargada de revisar disponibilidad en cuartos
    """
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