from django.core.management.base import BaseCommand
from pontos_turisticos.models import TouristSpot, City, CityType
import json
import os

class Command(BaseCommand):
    help = 'Import initial data for tourist spots'

    def handle(self, *args, **options):
        # Criar tipos de cidade
        city_types = [
            {'name': 'Capital'},
            {'name': 'Interior'},
            {'name': 'Litoral'},
            {'name': 'Serra'},
        ]
        
        for type_data in city_types:
            CityType.objects.get_or_create(name=type_data['name'])

        # Criar cidades
        cities = [
            {'name': 'São Paulo', 'type': 'Capital'},
            {'name': 'Campinas', 'type': 'Interior'},
            {'name': 'Santos', 'type': 'Litoral'},
            {'name': 'Campos do Jordão', 'type': 'Serra'},
        ]
        
        for city_data in cities:
            city_type = CityType.objects.get(name=city_data['type'])
            City.objects.get_or_create(
                name=city_data['name'],
                defaults={'type': city_type}
            )

        # Criar pontos turísticos
        spots = [
            {
                'name': 'Parque Ibirapuera',
                'description': 'Um dos principais parques urbanos de São Paulo',
                'city': 'São Paulo',
                'address': 'Av. Pedro Álvares Cabral',
                'image': 'pontos_turisticos/ibirapuera.jpg'
            },
            {
                'name': 'Lagoa do Taquaral',
                'description': 'Parque municipal com lagoa e área de lazer',
                'city': 'Campinas',
                'address': 'Av. Dr. Heitor Penteado',
                'image': 'pontos_turisticos/taquaral.jpg'
            },
            {
                'name': 'Praia do Gonzaga',
                'description': 'Uma das principais praias de Santos',
                'city': 'Santos',
                'address': 'Av. Ana Costa',
                'image': 'pontos_turisticos/gonzaga.jpg'
            },
            {
                'name': 'Morro do Elefante',
                'description': 'Mirante com vista panorâmica de Campos do Jordão',
                'city': 'Campos do Jordão',
                'address': 'Av. Pedro Paulo',
                'image': 'pontos_turisticos/elefante.jpg'
            }
        ]

        for spot_data in spots:
            city = City.objects.get(name=spot_data['city'])
            TouristSpot.objects.get_or_create(
                name=spot_data['name'],
                defaults={
                    'description': spot_data['description'],
                    'city': city,
                    'address': spot_data['address'],
                    'image': spot_data['image']
                }
            )

        self.stdout.write(self.style.SUCCESS('Initial data imported successfully')) 