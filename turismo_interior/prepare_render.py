import os
import django
import shutil
from pathlib import Path

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo_interior.settings')
django.setup()

from django.core.management import call_command
from pontos_turisticos.models import TouristSpot, Type, CityType, City

def main():
    print("Iniciando preparação para o Render...")
    
    # 1. Limpar banco de dados
    print("Limpando banco de dados...")
    TouristSpot.objects.all().delete()
    Type.objects.all().delete()
    CityType.objects.all().delete()
    City.objects.all().delete()
    
    # 2. Importar dados do CSV
    print("Importando dados do CSV...")
    try:
        csv_path = r"H:\univesp\Banco\pontos_turisticos_traduzido.csv"
        print(f"Tentando importar CSV de: {csv_path}")
        call_command('import_csv', csv_path=csv_path)
    except Exception as e:
        print(f"Erro ao importar CSV: {e}")
        return
    
    # 3. Exportar dados para JSON
    print("Exportando dados para JSON...")
    try:
        call_command('export_data')
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        return
    
    # 4. Copiar arquivos necessários
    print("Copiando arquivos...")
    base_dir = Path(__file__).resolve().parent
    
    # Copiar arquivos JSON para a pasta data
    data_dir = base_dir / 'data'
    if not data_dir.exists():
        data_dir.mkdir()
    
    # Copiar arquivos estáticos
    static_dir = base_dir / 'static'
    if not static_dir.exists():
        static_dir.mkdir()
    
    # 5. Criar arquivo .env para o Render
    env_content = """DEBUG=False
SECRET_KEY=django-insecure-mma@zaosporji5+&s&^o26o(7stw@8y*g$q8esyfvsg%0jd22)
ALLOWED_HOSTS=.onrender.com
"""
    with open(base_dir / '.env', 'w') as f:
        f.write(env_content)
    
    # 6. Atualizar .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Environment
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    with open(base_dir / '.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("Preparação concluída!")
    print("\nPróximos passos:")
    print("1. Faça commit das alterações:")
    print("   git add .")
    print("   git commit -m 'Preparando para deploy no Render'")
    print("2. Faça push para o GitHub:")
    print("   git push origin main")
    print("3. No Render.com, conecte seu repositório e faça o deploy")

if __name__ == '__main__':
    main() 