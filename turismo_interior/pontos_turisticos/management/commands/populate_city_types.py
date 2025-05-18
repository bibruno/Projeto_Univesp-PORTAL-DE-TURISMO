from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Este comando é um stub e não faz mais nada. Mantido para compatibilidade.'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('AVISO: O comando populate_city_types está obsoleto.')
        )
        self.stdout.write(
            self.style.WARNING('A tabela CityType não é mais utilizada. O sistema agora usa consultas dinâmicas.')
        )
        
        self.stdout.write(
            self.style.SUCCESS('Comando executado com sucesso (sem ações).')
        ) 