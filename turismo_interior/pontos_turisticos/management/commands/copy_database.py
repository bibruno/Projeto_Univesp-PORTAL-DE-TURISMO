from django.core.management.base import BaseCommand
import os
import shutil

class Command(BaseCommand):
    help = 'Copy the local database to the production environment'

    def handle(self, *args, **options):
        try:
            # Caminho do banco de dados local
            local_db = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db.sqlite3')
            
            # Caminho do banco de dados de produção
            prod_db = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db.sqlite3.prod')
            
            # Copiar o banco de dados
            shutil.copy2(local_db, prod_db)
            
            self.stdout.write(self.style.SUCCESS('Database copied successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error copying database: {str(e)}'))
            raise 