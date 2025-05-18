from django.core.management.base import BaseCommand
from django.core import serializers
import json
import os
from pontos_turisticos.models import TouristSpot, Type, CityType, City

class Command(BaseCommand):
    help = 'Importa dados do JSON para o banco'

    def handle(self, *args, **options):
        # Diretório onde estão os arquivos JSON
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        
        # Ordem de importação para respeitar as dependências
        models = [Type, CityType, City, TouristSpot]
        
        for model in models:
            filename = os.path.join(data_dir, f'{model.__name__.lower()}.json')
            
            if not os.path.exists(filename):
                self.stdout.write(self.style.WARNING(f'Arquivo não encontrado: {filename}'))
                continue
            
            # Limpar dados existentes
            model.objects.all().delete()
            
            # Ler e importar dados
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
                objects = serializers.deserialize('json', data)
                
                count = 0
                for obj in objects:
                    obj.save()
                    count += 1
                
                self.stdout.write(self.style.SUCCESS(f'Importados {count} registros de {model.__name__}')) 