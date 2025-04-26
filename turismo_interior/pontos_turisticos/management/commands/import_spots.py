import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from pontos_turisticos.models import TouristSpot, Type

class Command(BaseCommand):
    help = 'Importa pontos turísticos do CSV de forma otimizada'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {csv_path}'))
            return

        self.stdout.write('Iniciando importação...')
        
        # Primeiro, coletar todos os tipos únicos
        type_names = set()
        spots_data = []
        
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Limpar e normalizar os tipos
                types = [t.strip() for t in row['Tipos'].split(',')]
                type_names.update(types)
                spots_data.append({
                    'data': row,
                    'types': types
                })
        
        self.stdout.write(f'Encontrados {len(type_names)} tipos únicos')
        
        # Criar tipos em bulk
        Type.objects.bulk_create(
            [Type(name=name) for name in type_names],
            ignore_conflicts=True
        )
        
        # Mapear nomes de tipos para objetos Type
        type_map = {t.name: t for t in Type.objects.all()}
        
        # Criar spots em bulk
        spots = []
        for spot_info in spots_data:
            row = spot_info['data']
            try:
                spot = TouristSpot(
                    name=row['Nome'],
                    address=row['Endereço'],
                    city=row['Cidade'],
                    rating=float(row['Avaliação'].replace(',', '.')) if row['Avaliação'] else 0.0,
                    latitude=row['Latitude'].replace('.', '').replace(',', '.'),
                    longitude=row['Longitude'].replace('.', '').replace(',', '.'),
                    place_id=row['Place_ID']
                )
                spots.append(spot)
            except (ValueError, KeyError) as e:
                self.stdout.write(self.style.WARNING(f'Erro ao processar linha: {e}'))
                continue
        
        self.stdout.write(f'Importando {len(spots)} pontos turísticos...')
        TouristSpot.objects.bulk_create(spots, batch_size=1000)
        
        # Adicionar tipos aos spots
        for spot, spot_info in zip(spots, spots_data):
            types = [type_map[t] for t in spot_info['types'] if t in type_map]
            spot.types.add(*types)
        
        self.stdout.write(self.style.SUCCESS(f'Importação concluída! {len(spots)} pontos turísticos importados.')) 