from django.core.management.base import BaseCommand
from pontos_turisticos.models import TouristSpot

class Command(BaseCommand):
    help = 'Lista todas as cidades e seus respectivos tipos'

    def handle(self, *args, **options):
        # Obtém todas as cidades únicas
        cities = TouristSpot.objects.values_list('city', flat=True).distinct().order_by('city')
        
        for city in cities:
            self.stdout.write(f"\nCidade: {city}")
            self.stdout.write("-" * 50)
            
            # Obtém todos os pontos turísticos desta cidade
            spots = TouristSpot.objects.filter(city=city)
            
            # Coleta todos os tipos únicos para esta cidade
            types = set()
            for spot in spots:
                spot_types = spot.types.values_list('name', flat=True)
                types.update(spot_types)
            
            # Lista os tipos encontrados
            if types:
                for type_name in sorted(types):
                    self.stdout.write(f"  - {type_name}")
            else:
                self.stdout.write("  Nenhum tipo encontrado")
            
            # Mostra quantos pontos turísticos tem na cidade
            self.stdout.write(f"\n  Total de pontos turísticos: {spots.count()}") 