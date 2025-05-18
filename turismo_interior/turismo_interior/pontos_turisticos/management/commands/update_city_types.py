from django.core.management.base import BaseCommand
from django.db.models import Count
from pontos_turisticos.models import TouristSpot, CityTypes
from django.db import transaction, connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Atualiza a tabela CityTypes com os tipos de cada cidade'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando atualização da tabela CityTypes...')
        
        try:
            # Verifica se a tabela existe
            table_exists = False
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='pontos_turisticos_citytypes';"
                )
                if cursor.fetchone():
                    table_exists = True
            
            # Se a tabela não existir, cria as migrações e aplica
            if not table_exists:
                self.stdout.write('Tabela CityTypes não encontrada. Criando migrações...')
                call_command('makemigrations', 'pontos_turisticos')
                self.stdout.write('Aplicando migrações...')
                call_command('migrate', 'pontos_turisticos')
            
            with transaction.atomic():
                # Limpa a tabela atual
                if table_exists:
                    CityTypes.objects.all().delete()
                
                # Obtém todas as cidades
                cities = TouristSpot.objects.values_list('city', flat=True).distinct()
                self.stdout.write(f'Encontradas {len(cities)} cidades')
                
                # Para cada cidade, obtém os tipos e suas contagens
                total_relations = 0
                for city in cities:
                    # Obtém os tipos e suas contagens para esta cidade
                    types_count = (
                        TouristSpot.objects.filter(city=city)
                        .values('types__name')
                        .annotate(count=Count('id'))
                        .filter(types__name__isnull=False)
                    )
                    
                    # Cria os registros na tabela CityTypes
                    for type_count in types_count:
                        type_name = type_count['types__name']
                        count = type_count['count']
                        if type_name:  # Ignora tipos nulos
                            CityTypes.objects.create(
                                city=city,
                                type_name=type_name,
                                count=count
                            )
                            total_relations += 1
                    
                    self.stdout.write(f'Processada cidade: {city} - {len(types_count)} tipos')
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Atualização concluída! {total_relations} relações cidade-tipo criadas'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro durante a atualização: {str(e)}')
            )
            raise 