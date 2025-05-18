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
        # Criar CityType padrão se não existir
        default_city_type, _ = CityType.objects.get_or_create(name='Padrão')
        
        # Caminho relativo ao diretório do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        csv_path = os.path.join(base_dir, 'Banco', 'pontos_turisticos_traduzido.csv')
        
        self.stdout.write(f'Tentando abrir arquivo em: {csv_path}')
        
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    # Criar ou obter cidade
                    city_name = row['Cidade'].strip()
                    city, _ = City.objects.get_or_create(
                        name=city_name,
                        defaults={'type': default_city_type}
                    )
                    
                    # Criar ou atualizar ponto turístico
                    place_id = row['Place_ID'] if 'Place_ID' in row else None
                    if place_id:
                        spot, created = TouristSpot.objects.update_or_create(
                            place_id=place_id,
                            defaults={
                                'name': row['Nome'].strip(),
                                'description': row['Endereço'].strip(),
                                'city': city_name,  # Modelo espera string, não objeto
                                'address': row['Endereço'].strip(),
                                'rating': clean_number(row['Avaliação']) if 'Avaliação' in row else None,
                                'latitude': row['Latitude'].replace('.', '', row['Latitude'].count('.')-1) if 'Latitude' in row else '',
                                'longitude': row['Longitude'].replace('.', '', row['Longitude'].count('.')-1) if 'Longitude' in row else ''
                            }
                        )
                        
                        # Limpar tipos existentes e adicionar os novos
                        spot.types.clear()
                        tipos = [t.strip() for t in row['Tipos'].split(',') if t.strip()]
                        for tipo in tipos:
                            type_obj, _ = Type.objects.get_or_create(name=tipo)
                            spot.types.add(type_obj)
                        
                        count += 1
                        if count % 100 == 0:
                            self.stdout.write(f'Processados {count} pontos turísticos...')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro ao processar linha {count + 1}: {str(e)}'))
                    self.stdout.write(f'Dados da linha: {row}')
            
            self.stdout.write(self.style.SUCCESS(f'Processados {count} pontos turísticos do CSV.')) 