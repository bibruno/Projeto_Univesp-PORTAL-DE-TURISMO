import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo_interior.settings')
django.setup()

import csv
from pontos_turisticos.models import TouristSpot, Type

def clean_number(value):
    """Remove pontos extras de números e converte para float."""
    if not value:
        return 0.0
    # Remove todos os pontos exceto o último
    parts = value.rsplit('.', 1)
    if len(parts) == 2:
        return float(parts[0].replace('.', '') + '.' + parts[1])
    return float(value.replace('.', ''))

def import_spots():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'Banco', 'pontos_turisticos_traduzido.csv')
    
    print('Iniciando importação...')
    
    # Primeiro, vamos criar todos os tipos únicos
    types_set = set()
    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            types = row['Tipos'].split(',')
            types_set.update(type_name.strip() for type_name in types if type_name.strip())
    
    # Criar os tipos no banco de dados
    types_dict = {}
    for type_name in types_set:
        type_obj, created = Type.objects.get_or_create(name=type_name)
        types_dict[type_name] = type_obj
    
    print(f'Tipos criados: {len(types_dict)}')
    
    # Agora vamos criar os pontos turísticos
    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            try:
                # Criar o ponto turístico
                spot = TouristSpot.objects.create(
                    name=row['Nome'],
                    address=row['Endereço'],
                    city=row['Cidade'],
                    rating=clean_number(row['Avaliação'].replace(',', '.')) if row['Avaliação'] else 0.0,
                    latitude=clean_number(row['Latitude']),
                    longitude=clean_number(row['Longitude']),
                    place_id=row['Place_ID']
                )
                
                # Adicionar os tipos
                types = row['Tipos'].split(',')
                for type_name in types:
                    type_name = type_name.strip()
                    if type_name in types_dict:
                        spot.types.add(types_dict[type_name])
                
                count += 1
                if count % 100 == 0:
                    print(f'Importados {count} pontos turísticos...')
            except Exception as e:
                print(f'Erro ao importar linha {count + 1}: {e}')
                print(f'Dados da linha: {row}')
                continue
    
    print(f'Importação concluída! {count} pontos turísticos importados.')

if __name__ == '__main__':
    import_spots() 