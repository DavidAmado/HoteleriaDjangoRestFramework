from rest_framework import serializers
from reservation.models import Guest, Room, Reservation
class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['nombre', 'correo', 'telefono']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['numero']

class ReservationDictSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(many=False, queryset = Room.objects.all())
    guest = GuestSerializer(many=False)
    class Meta:
        model = Reservation
        fields = '__all__'
    def create(self, validated_data):
        """
        Modificamos el metodo para crear el Guest o devolverlo si fue creado previamente.
        """
        guest_data = validated_data.pop('guest')
        try:
            guest = Guest.objects.get(nombre=guest_data['nombre'], correo=guest_data['correo'])
        except Guest.DoesNotExist:
            guest = Guest.objects.create(nombre=guest_data['nombre'], correo=guest_data['correo'], telefono=guest_data['telefono'])
        
        reservation = Reservation.objects.create(guest=guest, **validated_data)
        return reservation
class ReservationIDSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(many=False, queryset = Room.objects.all())
    guest = serializers.PrimaryKeyRelatedField(many=False, queryset=Guest.objects.all())
    class Meta:
        model = Reservation
        fields = '__all__'
    