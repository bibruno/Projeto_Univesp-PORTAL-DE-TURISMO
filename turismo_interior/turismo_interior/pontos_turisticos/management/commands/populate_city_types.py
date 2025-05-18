from django.core.management.base import BaseCommand
from pontos_turisticos.models import TouristSpot, CityType

class Command(BaseCommand):
    help = 'Popula a tabela CityType com os tipos disponíveis por cidade'

    def handle(self, *args, **options):
        # Limpa dados existentes
        CityType.objects.all().delete()
        
        # Obtém todas as cidades únicas
        cities = TouristSpot.objects.values_list('city', flat=True).distinct()
        
        for city in cities:
            self.stdout.write(f"\nProcessando cidade: {city}")
            
            # Obtém todos os pontos turísticos desta cidade
            spots = TouristSpot.objects.filter(city=city)
            
            # Coleta todos os tipos únicos para esta cidade
            types = set()
            for spot in spots:
                spot_types = list(spot.types.values_list('name', flat=True))
                types.update(spot_types)
                self.stdout.write(f"  Ponto turístico: {spot.name}")
                self.stdout.write(f"  Tipos encontrados: {spot_types}")
            
            # Cria registros na tabela CityType
            for type_name in types:
                if type_name:  # Garante que o tipo não é None
                    CityType.objects.create(city=city, type=type_name)
                    self.stdout.write(f"  Adicionado tipo: {type_name}")
        
        # Verifica se os dados foram salvos
        total_registros = CityType.objects.count()
        self.stdout.write(f"\nTotal de registros na tabela CityType: {total_registros}")
        
        # Lista algumas amostras
        self.stdout.write("\nAmostra de registros:")
        for ct in CityType.objects.all()[:5]:
            self.stdout.write(f"  {ct.city} - {ct.type}")
        
        self.stdout.write(self.style.SUCCESS('\nTabela CityType populada com sucesso!')) 