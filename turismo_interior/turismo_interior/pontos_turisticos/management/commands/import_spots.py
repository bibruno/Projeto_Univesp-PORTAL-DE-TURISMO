import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from pontos_turisticos.models import TouristSpot, Type

class Command(BaseCommand):
    help = 'Importa pontos turísticos do CSV de forma otimizada'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')
        parser.add_argument('--clear', action='store_true', help='Limpar dados existentes antes de importar')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        clear_data = kwargs.get('clear', False)
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {csv_path}'))
            return

        self.stdout.write('Iniciando importação...')
        
        if clear_data:
            self.stdout.write('Limpando dados existentes...')
            TouristSpot.objects.all().delete()
            Type.objects.all().delete()
        
        type_names = set()
        spots_data = []
        
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                types = [t.strip() for t in row.get('Tipos', '').split(',') if t.strip()]
                type_names.update(types)
                spots_data.append({'data': row, 'types': types})
        
        self.stdout.write(f'Encontrados {len(type_names)} tipos únicos')
        
        try:
            with transaction.atomic():
                Type.objects.bulk_create(
                    [Type(name=name) for name in type_names],
                    ignore_conflicts=True
                )
        except IntegrityError as e:
            self.stdout.write(self.style.WARNING(f'Erro ao criar tipos (possivelmente já existem): {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro inesperado ao criar tipos: {e}'))
            return # Aborta se não conseguir criar tipos

        type_map = {t.name: t for t in Type.objects.all()}
        existing_place_ids = set(TouristSpot.objects.values_list('place_id', flat=True))
        self.stdout.write(f'Encontrados {len(existing_place_ids)} pontos turísticos existentes')
        
        spot_count = 0
        skipped = 0
        failed_rows = 0

        for spot_info in spots_data:
            row = spot_info['data']
            place_id = row.get('Place_ID')

            if not place_id:
                self.stdout.write(self.style.WARNING(f'Linha sem Place_ID, pulando: {row}'))
                failed_rows += 1
                continue
            
            if place_id in existing_place_ids:
                skipped += 1
                continue
                
            try:
                with transaction.atomic(): # Transação para cada spot
                    rating = float(row.get('Avaliação', '0').replace(',', '.')) if row.get('Avaliação') else 0.0
                    latitude = row.get('Latitude', '0').replace('.', '').replace(',', '.')
                    longitude = row.get('Longitude', '0').replace('.', '').replace(',', '.')

                    spot = TouristSpot.objects.create(
                        name=row.get('Nome', 'Sem nome'),
                        address=row.get('Endereço', ''),
                        city=row.get('Cidade', 'Desconhecida'),
                        rating=rating,
                        latitude=latitude,
                        longitude=longitude,
                        place_id=place_id
                    )
                    
                    spot_types_names = spot_info['types']
                    if spot_types_names:
                        types_to_add = [type_map[t_name] for t_name in spot_types_names if t_name in type_map]
                        if types_to_add:
                            spot.types.add(*types_to_add)
                    spot_count += 1

            except IntegrityError as e:
                self.stdout.write(self.style.WARNING(f'Erro de integridade ao processar {place_id} (possivelmente duplicado ou dados inválidos): {e}'))
                failed_rows +=1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao processar linha para {place_id}: {e}'))
                failed_rows +=1
                # Não relançar a exceção aqui para continuar processando outros spots
        
        if spot_count == 0 and skipped > 0 and failed_rows == 0:
            self.stdout.write(self.style.SUCCESS(f'Nenhum novo ponto turístico para importar. {skipped} pontos já existentes.'))
        elif spot_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Importação concluída! {spot_count} pontos turísticos importados.'))
        
        if skipped > 0:
            self.stdout.write(self.style.INFO(f'{skipped} pontos turísticos existentes foram pulados.'))
        if failed_rows > 0:
            self.stdout.write(self.style.ERROR(f'{failed_rows} linhas falharam ao serem processadas.')) 