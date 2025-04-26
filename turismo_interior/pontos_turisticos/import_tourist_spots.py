import csv
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo_interior.settings')
django.setup()

from pontos_turisticos.models import TouristSpot

CSV_PATH = os.path.join(os.path.dirname(__file__), '../../Banco/pontos_turisticos_traduzido.csv')

with open(CSV_PATH, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        TouristSpot.objects.create(
            name=row['Nome'],
            address=row['Endereço'],
            city=row['Cidade'],
            rating=float(row['Avaliação'].replace(',', '.')) if row['Avaliação'] else 0.0,
            types=row['Tipos'],
            latitude=row['Latitude'],
            longitude=row['Longitude'],
            place_id=row['Place_ID']
        )
print('Importação concluída!') 