from django.core.management.base import BaseCommand
from django.core import serializers
import json
from pontos_turisticos.models import TouristSpot, Type, CityType, City

class Command(BaseCommand):
    help = 'Exporta dados do banco SQLite para JSON'

    def handle(self, *args, **options):
        # Criar diretório data se não existir
        import os
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        os.makedirs(data_dir, exist_ok=True)

        # Exportar dados de cada modelo
        models = [TouristSpot, Type, CityType, City]
        
        for model in models:
            # Obter todos os objetos do modelo
            objects = model.objects.all()
            
            # Serializar para JSON
            data = serializers.serialize('json', objects)
            
            # Salvar em arquivo
            filename = os.path.join(data_dir, f'{model.__name__.lower()}.json')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            
            self.stdout.write(self.style.SUCCESS(f'Exportados {objects.count()} registros de {model.__name__}')) 