from django.db import models

class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    capacidade = models.IntegerField()

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    reservado_por = models.CharField(max_length=100)
    hora_inicio = models.DateTimeField()
    hora_termino = models.DateTimeField()
    proposito = models.TextField()

    def __str__(self):
        return f"Reserva de {self.sala} por {self.reservado_por}"
