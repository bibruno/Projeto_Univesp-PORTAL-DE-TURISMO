from django.core.management.base import BaseCommand
import csv
import os
from pontos_turisticos.models import TouristSpot, Type, City, CityType

def clean_number(value):
    """Remove pontos extras de números e converte para float."""
    if not value:
        return 0.0
    value = value.replace(',', '.')
    parts = value.rsplit('.', 1)
    if len(parts) == 2:
        return float(parts[0].replace('.', '') + '.' + parts[1])
    return float(value.replace('.', ''))

class Command(BaseCommand):
    help = 'Importa pontos turísticos do CSV para o banco de dados'

    def handle(self, *args, **options):
        csv_file = 'Banco/pontos_turisticos_traduzido.csv'
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'Arquivo {csv_file} não encontrado'))
            return

        # Criar tipo de cidade padrão se não existir
        default_city_type, _ = CityType.objects.get_or_create(name='Padrão')
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            total_rows = sum(1 for row in reader)
            file.seek(0)
            next(reader)  # Pular o cabeçalho
            
            imported_count = 0
            error_count = 0
            
            for i, row in enumerate(reader, start=2):
                try:
                    # Limpar e formatar os dados
                    name = row['Nome'].strip()
                    address = row['Endereço'].strip()
                    city_name = row['Cidade'].replace(', SP', '').strip()
                    rating = clean_number(row['Avaliação'])
                    types = [t.strip() for t in row['Tipos'].split(',')]
                    latitude = clean_number(row['Latitude'])
                    longitude = clean_number(row['Longitude'])
                    place_id = row['Place_ID'].strip()

                    # Criar ou obter a cidade
                    city, _ = City.objects.get_or_create(
                        name=city_name,
                        defaults={'type': default_city_type}
                    )

                    # Criar ou atualizar o ponto turístico
                    spot, created = TouristSpot.objects.update_or_create(
                        place_id=place_id,
                        defaults={
                            'name': name,
                            'description': f'Ponto turístico em {city_name}',
                            'city': city,
                            'address': address,
                            'rating': rating,
                            'latitude': latitude,
                            'longitude': longitude
                        }
                    )

                    # Limpar tipos existentes e adicionar os novos
                    spot.types.clear()
                    for type_name in types:
                        type_obj, _ = Type.objects.get_or_create(name=type_name)
                        spot.types.add(type_obj)

                    imported_count += 1
                    
                    if imported_count % 100 == 0:
                        self.stdout.write(f'Importados {imported_count} pontos turísticos...')
                        
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'Erro ao importar linha {i}: {str(e)}'))
                    self.stdout.write(self.style.ERROR(f'Dados da linha: {row}'))
                    continue

            self.stdout.write(self.style.SUCCESS(f'Importação concluída! {imported_count} pontos turísticos importados.'))
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f'Foram encontrados {error_count} erros durante a importação.')) 