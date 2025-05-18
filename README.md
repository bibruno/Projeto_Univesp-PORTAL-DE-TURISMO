# Portal de Turismo do Interior de SP

Portal web para visualização e busca de pontos turísticos do interior de São Paulo.

## 🌟 Funcionalidades

* **Listagem de Pontos Turísticos**  
   * Visualização em cards com informações detalhadas
   * Sistema de paginação
   * Links diretos para o Google Maps

* **Sistema de Filtros**  
   * Filtro por cidade
   * Filtro por tipo de ponto turístico
   * Filtros dinâmicos em cascata
   * Atualização em tempo real

* **Estatísticas**  
   * Total de pontos turísticos
   * Distribuição por cidade
   * Média de avaliações
   * Distribuição por tipo

## 🛠️ Tecnologias Utilizadas

* **Backend**  
   * Django 5.2  
   * Python 3.x  
   * SQLite (banco de dados)
   * Django ORM (Object-Relational Mapping)

* **Frontend**  
   * HTML5  
   * CSS3  
   * JavaScript  
   * Fetch API (para filtros dinâmicos)
   * Bootstrap 5.3  
   * Bootstrap Icons

* **Deploy**
   * Render.com (PaaS)
   * Gunicorn (servidor WSGI)

## 📋 Pré-requisitos

* Python 3.x
* pip (gerenciador de pacotes Python)
* Git (opcional)

## 🔧 Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/bibruno/Projeto_Univesp-PORTAL-DE-TURISMO.git
cd Projeto_Univesp-PORTAL-DE-TURISMO
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
cd turismo_interior/turismo_interior
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Importe os dados do CSV:
```bash
python manage.py import_spots ../../Banco/pontos_turisticos_traduzido.csv
```

6. Atualize o cache de tipos:
```bash
python manage.py update_city_types
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## 🌐 Deploy no Render.com

O projeto está configurado para deploy automático no Render.com. Quando novos commits são enviados para o repositório GitHub, o Render.com detecta automaticamente as alterações e inicia um novo deploy.

### Configuração do Render.com

O arquivo `render.yaml` na raiz do projeto contém todas as configurações necessárias para o deploy:

```yaml
services:
  - type: web
    name: turismo-interior
    env: python
    buildCommand: |
      cd turismo_interior/turismo_interior
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
      python manage.py import_spots ../../Banco/pontos_turisticos_traduzido.csv --clear
      python manage.py update_city_types
    startCommand: |
      cd turismo_interior/turismo_interior
      gunicorn turismo_interior.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        value: django-insecure-mma@zaosporji5+&s&^o26o(7stw@8y*g$q8esyfvsg%0jd22
      - key: DEBUG
        value: false
      - key: DJANGO_SETTINGS_MODULE
        value: turismo_interior.settings
```

## 🔧 Comandos de Manutenção

* **import_spots**: Importa pontos turísticos do CSV
  ```bash
  python manage.py import_spots caminho/do/arquivo.csv
  ```

* **update_city_types**: Atualiza a tabela de cache de tipos por cidade
  ```bash
  python manage.py update_city_types
  ```
  Este comando:
  1. Limpa a tabela `CityTypes` existente
  2. Obtém todas as cidades do sistema
  3. Para cada cidade, calcula os tipos e suas contagens
  4. Cria novos registros otimizados para consulta

## 🔍 Sistema de Filtro em Cascata

### Backend (views.py)
```python
def get_types_for_city(request):
    try:
        city = request.GET.get('city', '')
        
        if city == 'Todas':
            types = Type.objects.values_list('name', flat=True).distinct()
        else:
            city_name = city.replace(', SP', '')
            city_types = CityTypes.objects.filter(city_name__icontains=city_name)
            
            if city_types.exists():
                types = city_types.values_list('type_name', flat=True).distinct()
            else:
                types = Type.objects.filter(
                    touristspot__city__icontains=city_name
                ).values_list('name', flat=True).distinct()
                
                if not types:
                    try:
                        call_command('update_city_types')
                    except Exception as e:
                        logger.error(f"Erro ao atualizar tabela CityTypes: {str(e)}")
        
        types_list = list(types) if 'types' in locals() else []
        return JsonResponse(types_list, safe=False)
        
    except Exception as e:
        logger.error(f"Erro ao buscar tipos para cidade {city}: {str(e)}")
        return JsonResponse([], safe=False)
```

### Frontend (JavaScript)
```javascript
function updateTypes(city) {
    const typeSelect = document.getElementById('type');
    typeSelect.innerHTML = '<option value="Todos">Todos</option>';
    
    if (city === 'Todas') {
        return;
    }
    
    fetch(`/api/types-for-city/?city=${encodeURIComponent(city)}`)
        .then(response => response.json())
        .then(types => {
            types.forEach(type => {
                const option = document.createElement('option');
                option.value = type;
                option.textContent = type;
                typeSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Erro ao buscar tipos:', error);
        });
}

// Evento com debounce
document.getElementById('city').addEventListener('change', 
    debounce(function() {
        updateTypes(this.value);
    }, 300)
);
```

## ⚠️ Solução de Problemas

### Tipos não aparecem para uma cidade
1. Verifique se há pontos turísticos cadastrados para a cidade
2. Execute o comando `update_city_types` para atualizar o cache
3. Verifique os logs do servidor para possíveis erros

### Erros de importação
1. Verifique se o arquivo CSV está no formato correto
2. Certifique-se de que o arquivo está acessível
3. Verifique os logs para mensagens de erro específicas

### Problemas de deploy
1. Verifique se todas as variáveis de ambiente estão configuradas
2. Certifique-se de que o arquivo `render.yaml` está atualizado
3. Verifique os logs do deploy no Render.com

## 📝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Agradecimentos

* UNIVESP
* Equipe de desenvolvimento
* Contribuidores
* Comunidade Open Source

