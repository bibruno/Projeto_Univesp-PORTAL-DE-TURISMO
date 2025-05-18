import requests
import time
import logging
from datetime import datetime

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)

# URL do seu site no Render.com
SITE_URL = "https://portal-turismo-interior-krvv.onrender.com"

def ping_site():
    """Faz uma requisição GET para o site."""
    try:
        response = requests.get(SITE_URL)
        if response.status_code == 200:
            logging.info(f"Site acessado com sucesso! Status: {response.status_code}")
        else:
            logging.warning(f"Site retornou status inesperado: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro ao acessar o site: {str(e)}")

def main():
    """Função principal que executa o ping periodicamente."""
    logging.info("Iniciando script de keep-alive...")
    
    while True:
        try:
            ping_site()
            # Aguarda 14 minutos antes da próxima requisição
            # (O Render.com hiberna após 15 minutos de inatividade)
            time.sleep(14 * 60)
        except KeyboardInterrupt:
            logging.info("Script interrompido pelo usuário.")
            break
        except Exception as e:
            logging.error(f"Erro inesperado: {str(e)}")
            time.sleep(60)  # Aguarda 1 minuto em caso de erro

if __name__ == "__main__":
    main() 