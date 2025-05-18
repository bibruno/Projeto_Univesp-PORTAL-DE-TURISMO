import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from pontos_turisticos.models import TouristSpot, Type

class Command(BaseCommand):
    help = 'Importa pontos turísticos do CSV de forma otimizada'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')
        parser.add_argument('--clear', action='store_true', help='Limpar dados existentes antes de importar')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        clear_data = kwargs.get('clear', False)
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {csv_path}'))
            return

        self.stdout.write('Iniciando importação...')
        
        # Limpar dados existentes se solicitado
        if clear_data:
            self.stdout.write('Limpando dados existentes...')
            TouristSpot.objects.all().delete()
            Type.objects.all().delete()
        
        # Primeiro, coletar todos os tipos únicos
        type_names = set()
        spots_data = []
        
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Limpar e normalizar os tipos
                types = [t.strip() for t in row.get('Tipos', '').split(',') if t.strip()]
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
        
        # Manter controle de place_ids existentes
        existing_place_ids = set(TouristSpot.objects.values_list('place_id', flat=True))
        self.stdout.write(f'Encontrados {len(existing_place_ids)} pontos turísticos existentes')
        
        # Criar spots individualmente para garantir que tenham IDs
        spot_count = 0
        skipped = 0
        
        for spot_info in spots_data:
            row = spot_info['data']
            try:
                place_id = row.get('Place_ID')
                if not place_id:
                    self.stdout.write(self.style.WARNING(f'Linha sem Place_ID, pulando: {row}'))
                    continue
                
                # Pular se já existir
                if place_id in existing_place_ids:
                    skipped += 1
                    continue
                    
                # Garantindo que dados numéricos são tratados corretamente
                try:
                    rating = float(row.get('Avaliação', '0').replace(',', '.'))
                except ValueError:
                    rating = 0.0
                    
                try:
                    latitude = row.get('Latitude', '0').replace('.', '').replace(',', '.')
                    longitude = row.get('Longitude', '0').replace('.', '').replace(',', '.')
                except Exception:
                    latitude = '0'
                    longitude = '0'
                    
                # Criamos e salvamos cada spot individualmente
                spot = TouristSpot(
                    name=row.get('Nome', 'Sem nome'),
                    address=row.get('Endereço', ''),
                    city=row.get('Cidade', 'Desconhecida'),
                    rating=rating,
                    latitude=latitude,
                    longitude=longitude,
                    place_id=place_id
                )
                
                # Salvar o spot para garantir que tenha um ID
                spot.save()
                
                # Adicionar tipos diretamente após salvar
                spot_types = [type_map[t] for t in spot_info['types'] if t in type_map]
                if spot_types:
                    spot.types.add(*spot_types)
                    spot_count += 1
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Erro ao processar linha: {e}'))
                continue
        
        if spot_count == 0 and skipped > 0:
            self.stdout.write(self.style.SUCCESS(f'Nenhum novo ponto turístico para importar. {skipped} pontos já existentes.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Importação concluída! {spot_count} pontos turísticos importados (pulando {skipped} existentes).')) 