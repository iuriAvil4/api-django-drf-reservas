from rest_framework import serializers
from .models import Sala, Reserva

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = "__all__"
    
class ReservaSerializer(serializers.ModelSerializer):

    hora_inicio = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    hora_termino = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Reserva
        fields = ['id_reserva', 'reservado_por', 'hora_inicio', 'hora_termino', 'proposito', 'sala']