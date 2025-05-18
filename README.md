# Portal de Turismo do Interior de São Paulo

Um portal web desenvolvido em Django para explorar pontos turísticos do interior de São Paulo, com filtros dinâmicos, estatísticas e integração com Google Maps.

## 🚀 Funcionalidades

* **Listagem de Pontos Turísticos**  
   * Visualização em cards com informações detalhadas  
   * Paginação (9 itens por página)  
   * Filtros dinâmicos por cidade e tipo  
   * Integração com Google Maps

* **Sistema de Filtro em Cascata**
   * Atualização dinâmica dos tipos disponíveis por cidade
   * Sistema de fallback em 3 níveis:
     1. Busca exata na tabela de cache
     2. Busca parcial com correspondência parcial
     3. Busca direta nos pontos turísticos
   * Debounce no frontend para otimização
   * Manutenção automática do cache
   * Logging detalhado para diagnóstico
   * Tratamento inteligente de nomes de cidade (com/sem ", SP")

* **Sistema de Cache de Tipos por Cidade**
   * Tabela `CityTypes` para armazenamento eficiente
   * Atualização automática via comando `update_city_types`
   * Contagem de pontos turísticos por tipo em cada cidade
   * Índices otimizados para consulta rápida

* **Filtros Inteligentes**  
   * Filtro por cidade com suporte a variações de nome
   * Busca case-insensitive para maior flexibilidade
   * Filtro de tipos que se atualiza automaticamente
   * Sistema de fallback para busca de tipos
   * Manutenção dos filtros durante a navegação

* **Estatísticas**  
   * Total de pontos turísticos  
   * Total de cidades  
   * Média de avaliações  
   * Top 10 cidades com mais pontos turísticos  
   * Distribuição por tipo

* **Interface Responsiva**  
   * Design moderno com Bootstrap  
   * Cards com efeito hover  
   * Badges para tipos  
   * Layout adaptável para diferentes dispositivos

* **Debugging Avançado**  
   * Painel de debug embutido na interface
   * Logs detalhados de requisições AJAX
   * Visualização de resposta da API em tempo real
   * Sistema de logging para diagnóstico de problemas

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
      python manage.py import_spots ../../Banco/pontos_turisticos_traduzido.csv
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
    city = request.GET.get('city', '')
    
    if not city or city == 'Todas':
        # Retorna todos os tipos se nenhuma cidade selecionada
        types = Type.objects.values_list('name', flat=True).distinct()
    else:
        # Remove sufixo ", SP" se existir
        city_name = city.replace(', SP', '')
        
        # Sistema de fallback em 3 níveis
        city_types = CityTypes.objects.filter(city__iexact=city_name)
        if not city_types.exists():
            city_types = CityTypes.objects.filter(city__icontains=city_name)
        
        if city_types.exists():
            types = city_types.values_list('type_name', flat=True).distinct()
        else:
            types = Type.objects.filter(
                touristspot__city__icontains=city_name
            ).values_list('name', flat=True).distinct()
```

### Frontend (JavaScript)
```javascript
function updateTypes(city) {
    const typeSelect = document.getElementById('type');
    const currentType = typeSelect.value;
    
    fetch(`/api/types-for-city/?city=${encodeURIComponent(city)}`)
        .then(response => response.json())
        .then(types => {
            types.forEach(type => {
                if (type) {
                    const option = document.createElement('option');
                    option.value = type;
                    option.textContent = type;
                    typeSelect.appendChild(option);
                }
            });
            
            if (currentType && types.includes(currentType)) {
                typeSelect.value = currentType;
            }
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
2. Execute o comando `update_city_types` para reconstruir o cache
3. Verifique os logs para mais detalhes do problema
4. Confirme se o nome da cidade está correto (com ou sem ", SP")

### Erro na importação de dados
1. Verifique se o arquivo CSV está no formato correto
2. Execute a importação com `--verbosity 2` para mais detalhes
3. Após a importação, execute `update_city_types`
4. Verifique se todos os tipos foram importados corretamente

### Performance dos Filtros
* A tabela `CityTypes` mantém um cache dos tipos por cidade
* As consultas são otimizadas com índices nas colunas `city` e `type_name`
* O sistema atualiza automaticamente o cache quando necessário
* Fallback para busca direta caso o cache esteja desatualizado

### Logs e Debugging
* Painel de debug na interface mostra detalhes das chamadas
* Logs do backend registram todas as operações
* Sistema de fallback registra cada nível de busca
* Contadores de performance para diagnóstico

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

