from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Sala, Reserva
from .serializers import SalaSerializer, ReservaSerializer

import json


@api_view(['GET'])
def get_salas(request):
    if request.method == 'GET':
        salas = Sala.objects.all().order_by("id_sala")

        # Parâmetros de consulta para pesquisa
        nome = request.GET.get('nome')
        localizacao = request.GET.get('localizacao')
        capacidade_min = request.GET.get('capacidade_min')
        capacidade_max = request.GET.get('capacidade_max')

        # Filtragem dos resultados
        if nome:
            salas = salas.filter(nome__icontains=nome)
        if localizacao:
            salas = salas.filter(localizacao__icontains=localizacao)
        if capacidade_min:
            salas = salas.filter(capacidade__gte=capacidade_min)
        if capacidade_max:
            salas = salas.filter(capacidade__lte=capacidade_max)

        # Paginação
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        paginator = Paginator(salas, page_size)

        try:
            salas_paginated = paginator.page(page)
        except PageNotAnInteger:
            salas_paginated = paginator.page(1)
        except EmptyPage:
            salas_paginated = paginator.page(paginator.num_pages)

        serializer = SalaSerializer(salas_paginated, many=True)

        response = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': salas_paginated.number,
            'page_size': page_size,
            'results': serializer.data,
        }

        return Response(response)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_reservas(request):
    if request.method == 'GET':
        reservas = Reserva.objects.all().order_by("id_reserva")

        # Parâmetros de consulta para pesquisa
        reservado_por = request.GET.get('reservado_por')
        hora_inicio_min = request.GET.get('hora_inicio_min')
        hora_inicio_max = request.GET.get('hora_inicio_max')
        hora_termino_min = request.GET.get('hora_termino_min')
        hora_termino_max = request.GET.get('hora_termino_max')
        proposito = request.GET.get('proposito')
        sala = request.GET.get('sala')

        # Filtragem dos resultados
        if reservado_por:
            reservas = reservas.filter(reservado_por__icontains=reservado_por)
        if hora_inicio_min:
            reservas = reservas.filter(hora_inicio__gte=hora_inicio_min)
        if hora_inicio_max:
            reservas = reservas.filter(hora_inicio__lte=hora_inicio_max)
        if hora_termino_min:
            reservas = reservas.filter(hora_termino__gte=hora_termino_min)
        if hora_termino_max:
            reservas = reservas.filter(hora_termino__lte=hora_termino_max)
        if proposito:
            reservas = reservas.filter(proposito__icontains=proposito)
        if sala:
            reservas = reservas.filter(sala=sala)

        # Paginação
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        paginator = Paginator(reservas, page_size)

        try:
            reservas_paginated = paginator.page(page)
        except PageNotAnInteger:
            reservas_paginated = paginator.page(1)
        except EmptyPage:
            reservas_paginated = paginator.page(paginator.num_pages)

        serializer = ReservaSerializer(reservas_paginated, many=True)

        response = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': reservas_paginated.number,
            'page_size': page_size,
            'results': serializer.data,
        }

        return Response(response)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def sala_manage(request):

    if request.method == 'GET':
        try:
            id_sala = request.GET.get('id_sala')
            if id_sala is not None:
                try:
                    sala = Sala.objects.get(pk=id_sala)
                    serializer = SalaSerializer(sala)
                    return Response(serializer.data)
                except Sala.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Parâmetro 'id_sala' é obrigatório."})
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Parâmetro 'id_sala' inválido."})

    if request.method == 'POST':
        new_sala = request.data
        serializer = SalaSerializer(data=new_sala)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        id_sala = request.data.get('id_sala')
        if id_sala is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Parâmetro 'id_sala' é obrigatório."})
        try: 
            updated_sala = Sala.objects.get(pk=id_sala)
        except Sala.DoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SalaSerializer(updated_sala, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    if request.method == 'DELETE':
        id_sala = request.GET.get('id_sala') or request.data.get('id_sala')
        if id_sala:
            try:
                sala_to_delete = Sala.objects.get(pk=id_sala)
                sala_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Sala.DoesNotExist:
                return Response({"message": "Sala não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Parâmetro 'id_sala' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def reserva_manage(request):

    if request.method == 'GET':
        id_reserva = request.GET.get('id_reserva')
        if id_reserva is not None:
            try:
                reserva = Reserva.objects.get(pk=id_reserva)
                serializer = ReservaSerializer(reserva)
                return Response(serializer.data)
            except Reserva.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Parâmetro 'id_reserva' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        id_reserva = request.data.get('id_reserva')
        if id_reserva is None:
            return Response({"message": "Parâmetro 'id_reserva' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reserva = Reserva.objects.get(pk=id_reserva)
        except Reserva.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id_reserva = request.GET.get('id_reserva') or request.data.get('id_reserva')
        if id_reserva:
            try:
                reserva_to_delete = Reserva.objects.get(pk=id_reserva)
                reserva_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Reserva.DoesNotExist:
                return Response({"message": "Reserva não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Parâmetro 'id_reserva' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)



