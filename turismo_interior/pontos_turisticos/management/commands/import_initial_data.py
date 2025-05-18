from django.core.management.base import BaseCommand
from pontos_turisticos.models import TouristSpot
import json
import os

class Command(BaseCommand):
    help = 'Import initial data for tourist spots'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Starting data import...')
            
            # Criar pontos turísticos
            spots = [
                {
                    'name': 'Parque Ibirapuera',
                    'description': 'Um dos principais parques urbanos de São Paulo',
                    'city': 'São Paulo',
                    'address': 'Av. Pedro Álvares Cabral'
                },
                {
                    'name': 'Lagoa do Taquaral',
                    'description': 'Parque municipal com lagoa e área de lazer',
                    'city': 'Campinas',
                    'address': 'Av. Dr. Heitor Penteado'
                },
                {
                    'name': 'Praia do Gonzaga',
                    'description': 'Uma das principais praias de Santos',
                    'city': 'Santos',
                    'address': 'Av. Ana Costa'
                },
                {
                    'name': 'Morro do Elefante',
                    'description': 'Mirante com vista panorâmica de Campos do Jordão',
                    'city': 'Campos do Jordão',
                    'address': 'Av. Pedro Paulo'
                }
            ]

            for spot_data in spots:
                obj, created = TouristSpot.objects.get_or_create(
                    name=spot_data['name'],
                    defaults={
                        'description': spot_data['description'],
                        'city': spot_data['city'],
                        'address': spot_data['address']
                    }
                )
                if created:
                    self.stdout.write(f'Created tourist spot: {spot_data["name"]}')
                else:
                    self.stdout.write(f'Tourist spot already exists: {spot_data["name"]}')

            self.stdout.write(self.style.SUCCESS('Initial data imported successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
            raise 