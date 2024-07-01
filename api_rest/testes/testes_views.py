from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..models import Sala, Reserva
from django.urls import reverse
import json

class GetSalasTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Criação de salas para o teste
        self.sala1 = Sala.objects.create(nome="Sala 1", 
                                         localizacao="Local A", 
                                         capacidade=10)
        self.sala2 = Sala.objects.create(nome="Sala 2", 
                                         localizacao="Local B", 
                                         capacidade=20)
        self.sala1.save()
        self.sala2.save()

    def test_get_salas(self):
        response = self.client.get(reverse('get_salas'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_get_salas_search_nome(self):
        response = self.client.get(reverse('get_salas'))
        self.assertEqual(response.data['results'][0]['nome'], self.sala1.nome)
        self.assertEqual(response.data['results'][1]['nome'], self.sala2.nome)
    
    def test_get_salas_search_localizacao(self):
        response = self.client.get(reverse('get_salas'))
        self.assertEqual(response.data['results'][0]['localizacao'], self.sala1.localizacao)
        self.assertEqual(response.data['results'][1]['localizacao'], self.sala2.localizacao)

    def test_get_salas_search_capacidade(self):
        response = self.client.get(reverse('get_salas'))
        self.assertEqual(response.data['results'][0]['capacidade'], self.sala1.capacidade)
        self.assertEqual(response.data['results'][1]['capacidade'], self.sala2.capacidade)
        
    def test_filter_salas_by_name(self):
        response = self.client.get(reverse('get_salas'), {'nome': 'Sala 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['nome'], 'Sala 1')

    def test_pagination(self):
        response = self.client.get(reverse('get_salas'), {'page_size': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['total_pages'], 2)
        self.assertEqual(len(response.data['results']), 1)

class GetReservasTestCase(TestCase):
    def setUp(self):
        self.cliente = APIClient()

        self.sala = Sala.objects.create(id_sala=1,
                                        nome="Sala TI", 
                                        localizacao="Local A", 
                                        capacidade=10)
        
        self.reserva1 = Reserva.objects.create(reservado_por="Lorem", 
                                               hora_inicio="2024-05-21 12:00:00", 
                                               hora_termino="2024-05-21 16:00:00",
                                               proposito="Tasks",
                                               sala=self.sala)
        self.reserva2 = Reserva.objects.create(reservado_por="Ipsum",
                                               hora_inicio="2024-06-21 12:00:00",
                                               hora_termino="2024-06-21 16:00:00",
                                               proposito="Tasks",
                                               sala=self.sala)
        self.reserva1.save()
        self.reserva2.save()

    def test_get_reservas(self):
        response = self.client.get(reverse('get_reservas'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_reservas_search_reservado_por(self):
        response = self.client.get(reverse('get_reservas'))
        self.assertEqual(response.data['results'][0]['reservado_por'], self.reserva1.reservado_por)
        self.assertEqual(response.data['results'][1]['reservado_por'], self.reserva2.reservado_por)
    
    def test_get_reservas_search_proposito(self):
        response = self.client.get(reverse('get_reservas'))
        self.assertEqual(response.data['results'][0]['proposito'], self.reserva1.proposito)
        self.assertEqual(response.data['results'][1]['proposito'], self.reserva2.proposito)
    
    def test_get_reservas_search_sala(self):
        response = self.client.get(reverse('get_reservas'))
        self.assertEqual(response.data['results'][0]['sala'], self.sala.id_sala)
        self.assertEqual(response.data['results'][1]['sala'], self.sala.id_sala)

    def test_get_reservas_search_hora_inicio(self):
        response = self.client.get(reverse('get_reservas'))
        self.assertEqual(response.data['results'][0]['hora_inicio'], self.reserva1.hora_inicio)
        self.assertEqual(response.data['results'][1]['hora_inicio'], self.reserva2.hora_inicio)

    def test_get_reservas_search_hora_termino(self):
        response = self.client.get(reverse('get_reservas'))
        self.assertEqual(response.data['results'][0]['hora_termino'], self.reserva1.hora_termino)
        self.assertEqual(response.data['results'][1]['hora_termino'], self.reserva2.hora_termino)


class ReservaManageTestCase(APITestCase):
    def setUp(self):
        self.headerInfo = {'content-type': 'application/json'}

        self.sala = Sala.objects.create(id_sala=1,
                                        nome="Sala TI", 
                                        localizacao="Local A", 
                                        capacidade=10)
        
        self.reserva1 = Reserva.objects.create(id_reserva=1,
                                               reservado_por="Lorem", 
                                               hora_inicio="2024-05-21 12:00:00", 
                                               hora_termino="2024-05-21 16:00:00",
                                               proposito="Tasks",
                                               sala=self.sala)
        self.reserva2 = Reserva.objects.create(id_reserva=2,
                                               reservado_por="Ipsum",
                                               hora_inicio="2024-06-21 12:00:00",
                                               hora_termino="2024-06-21 16:00:00",
                                               proposito="Taskss",
                                               sala=self.sala)
        self.reserva1.save()
        self.reserva2.save()

        self.reserva_data = {
            'reservado_por': 'Dolor',
            'hora_inicio': '2024-06-26 11:30:00',
            'hora_termino': '2024-06-26 16:00:00',
            'proposito': 'Tasksss',
            'sala': self.sala.id_sala
        }

        self.reserva_update_data = {
            'id_reserva': self.reserva1.id_reserva,
            'reservado_por': 'Lorem Updated',
            'hora_inicio': '2024-06-26T11:30:00Z',
            'hora_termino': '2024-06-26T16:00:00Z',
            'proposito': 'Tasksss',
            'sala': self.sala.id_sala
        }

        self.url_reserva_manage = reverse('reserva_manage')


    def test_get_valid_reserva(self):
        """GET method for valid reserva"""
        response = self.client.get(self.url_reserva_manage, {'id_reserva': self.reserva1.id_reserva}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_reserva(self):
        """GET method for invalid reserva"""
        response = self.client.get(self.url_reserva_manage, {'id_reserva': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_reserva_no_id(self):
        """GET method without id_reserva"""
        response = self.client.get(self.url_reserva_manage, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_reserva(self):
        """POST method for creating a reserva"""
        response = self.client.post(self.url_reserva_manage, data=json.dumps(self.reserva_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reserva.objects.count(), 3)

    def test_create_invalid_reserva(self):
        """POST method with invalid data"""
        invalid_data = self.reserva_data.copy()
        invalid_data['reservado_por'] = ''
        response = self.client.post(self.url_reserva_manage, data=json.dumps(invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_reserva(self):
        """PUT method for updating a reserva"""
        response = self.client.put(self.url_reserva_manage, data=json.dumps(self.reserva_update_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.reserva1.refresh_from_db()
        self.assertEqual(self.reserva1.reservado_por, 'Lorem Updated')
        self.assertEqual(self.reserva1.hora_inicio.strftime('%Y-%m-%dT%H:%M:%SZ'), '2024-06-26T11:30:00Z')
        self.assertEqual(self.reserva1.hora_termino.strftime('%Y-%m-%dT%H:%M:%SZ'), '2024-06-26T16:00:00Z')
        self.assertEqual(self.reserva1.proposito, 'Tasksss')
        self.assertEqual(self.reserva1.sala.id_sala, self.sala.id_sala)
        
    def test_update_invalid_reserva(self):
        """PUT method with invalid id"""
        invalid_update_reserva = self.reserva_update_data.copy()
        invalid_update_reserva['id_reserva'] = 999
        response = self.client.put(self.url_reserva_manage, data=json.dumps(invalid_update_reserva), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_reserva_no_id(self):
        """PUT method without id_reserva"""
        update_data_no_id = {
            'reservado_por': 'Lorem Updated',
            'hora_inicio': '2024-06-26T11:30:00Z',
            'hora_termino': '2024-06-26T16:00:00Z',
            'proposito': 'Tasksss',
            'sala': self.sala.id_sala
        }
        response = self.client.put(self.url_reserva_manage, data=json.dumps(update_data_no_id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_valid_reserva(self):
        """DELETE method for valid reserva"""
        response = self.client.delete(self.url_reserva_manage, data=json.dumps({'id_reserva': self.reserva1.id_reserva}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reserva.objects.count(), 1)


    def test_delete_invalid_sala(self):
        """DELETE method with invalid id"""
        response = self.client.delete(self.url_reserva_manage, data=json.dumps({'id_reserva': 999}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_sala_no_id(self):
        """DELETE method without id_sala"""
        response = self.client.delete(self.url_reserva_manage, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SalaManageTestCase(APITestCase):

    def setUp(self):
        self.headerInfo = {'content-type': 'application/json'}

        self.sala1 = Sala.objects.create(id_sala=1,
                                         nome="Sala 1",
                                         localizacao="Local 1",
                                         capacidade=10)
        self.sala2 = Sala.objects.create(id_sala=2,
                                         nome="Sala 2",
                                         localizacao="Local 2",
                                         capacidade=20)
        self.sala1.save()
        self.sala2.save()


        self.sala_data = {
            'nome': 'Sala 3',
            'localizacao': 'Local 3',
            'capacidade': 30
        }

        self.sala_update_data = {
            'id_sala': self.sala1.id_sala,
            'nome': 'Sala 1 Updated',
            'localizacao': 'Local 1 Updated',
            'capacidade': 15
        }

        self.url_sala_manage = reverse('sala_manage')


    def test_get_valid_sala(self):
        """GET method for valid sala"""
        response = self.client.get(self.url_sala_manage, {'id_sala': self.sala1.id_sala}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_sala(self):
        """GET method for invalid sala"""
        response = self.client.get(self.url_sala_manage, {'id_sala': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_sala_no_id(self):
        """GET method without id_sala"""
        response = self.client.get(self.url_sala_manage, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_sala(self):
        """POST method for creating a sala"""
        response = self.client.post(self.url_sala_manage, data=json.dumps(self.sala_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sala.objects.count(), 3)

    def test_create_invalid_sala(self):
        """POST method with invalid data"""
        invalid_data = self.sala_data.copy()
        invalid_data['nome'] = ''
        response = self.client.post(self.url_sala_manage, data=json.dumps(invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_sala(self):
        """PUT method for updating a sala"""
        response = self.client.put(self.url_sala_manage, data=json.dumps(self.sala_update_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.sala1.refresh_from_db()
        self.assertEqual(self.sala1.nome, 'Sala 1 Updated')
        self.assertEqual(self.sala1.localizacao, 'Local 1 Updated')
        self.assertEqual(self.sala1.capacidade, 15)

    def test_update_invalid_sala(self):
        """PUT method with invalid id"""
        invalid_update_data = self.sala_update_data.copy()
        invalid_update_data['id_sala'] = 999
        response = self.client.put(self.url_sala_manage, data=json.dumps(invalid_update_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_sala_no_id(self):
        """PUT method without id_sala"""
        update_data_no_id = {
            'nome': 'Sala Updated',
            'localizacao': 'Local Updated',
            'capacidade': 15
        }
        response = self.client.put(self.url_sala_manage, data=json.dumps(update_data_no_id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_sala(self):
        """DELETE method for valid sala"""
        response = self.client.delete(self.url_sala_manage, data=json.dumps({'id_sala': self.sala1.id_sala}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sala.objects.count(), 1)

    def test_delete_invalid_sala(self):
        """DELETE method with invalid id"""
        response = self.client.delete(self.url_sala_manage, data=json.dumps({'id_sala': 999}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_sala_no_id(self):
        """DELETE method without id_sala"""
        response = self.client.delete(self.url_sala_manage, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

