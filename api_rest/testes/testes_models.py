from ..models import Sala, Reserva
from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime

class TestModels(TestCase):

    def test_sala_model(self):
        sala = Sala.objects.create(nome="teste1", 
                                   localizacao="local1", 
                                   capacidade=10)
        sala.save()

        self.assertEqual(sala.nome, "teste1")
        self.assertEqual(sala.localizacao, "local1")
        self.assertEqual(sala.capacidade, 10)

    def test_reserva_model(self):
        sala = Sala.objects.create(nome="teste2", 
                                   localizacao="local2", 
                                   capacidade=20)
        sala.save()

        hora_inicio = make_aware(datetime.strptime("2024-05-23 10:00:00", "%Y-%m-%d %H:%M:%S"))
        hora_termino = make_aware(datetime.strptime("2024-05-23 16:00:00", "%Y-%m-%d %H:%M:%S"))

        reserva = Reserva.objects.create(sala=sala, 
                                         reservado_por="teste1", 
                                         hora_inicio=hora_inicio,
                                         hora_termino=hora_termino,
                                         proposito="teste1")
        reserva.save()

        self.assertEqual(reserva.sala, sala)
        self.assertEqual(reserva.reservado_por, "teste1")
        self.assertEqual(reserva.hora_inicio, hora_inicio)
        self.assertEqual(reserva.hora_termino, hora_termino)
        self.assertEqual(reserva.proposito, "teste1")
