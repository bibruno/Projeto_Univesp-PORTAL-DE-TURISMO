# Portal de Turismo do Interior de São Paulo

Um portal web desenvolvido em Django para explorar pontos turísticos do interior de São Paulo, com filtros dinâmicos, estatísticas e integração com Google Maps.

## 🚀 Funcionalidades

* **Listagem de Pontos Turísticos**  
   * Visualização em cards com informações detalhadas  
   * Paginação (9 itens por página)  
   * Filtros dinâmicos por cidade e tipo  
   * Integração com Google Maps
* **Filtros Inteligentes**  
   * Filtro por cidade  
   * Filtro por tipo que se atualiza automaticamente baseado na cidade selecionada  
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

6. Popule a tabela de tipos por cidade:
```bash
python manage.py populate_city_types
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
      python manage.py populate_city_types
    startCommand: |
      cd turismo_interior/turismo_interior
      gunicorn turismo_interior.wsgi:application
```

### Passos para Deploy Manual

1. Crie uma conta no [Render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Crie um novo Web Service e selecione o repositório
4. O Render.com detectará automaticamente o arquivo `render.yaml` e configurará o serviço
5. Clique em "Create Web Service" para iniciar o deploy

## 📊 Estrutura do Projeto

```
Projeto_Univesp-PORTAL-DE-TURISMO/
├── Banco/
│   └── pontos_turisticos_traduzido.csv
├── turismo_interior/
│   ├── turismo_interior/
│   │   ├── pontos_turisticos/
│   │   │   ├── migrations/
│   │   │   ├── templates/
│   │   │   │   ├── pontos_turisticos/
│   │   │   │       ├── base.html
│   │   │   │       ├── list.html
│   │   │   │       └── statistics.html
│   │   │   ├── management/
│   │   │   │   └── commands/
│   │   │   │       ├── import_spots.py
│   │   │   │       └── populate_city_types.py
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── turismo_interior/
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── manage.py
│   │   └── requirements.txt
├── render.yaml
└── README.md
```

## 🏗️ Arquitetura do Sistema

### Modelos de Dados

* **Type**: Define os tipos de pontos turísticos (ex: Museu, Parque)
* **TouristSpot**: Representa os pontos turísticos, com relacionamento many-to-many com Type
* **CityType**: (Legado) Originalmente usado para armazenar tipos disponíveis por cidade

### API e Endpoints

* **`/`**: Página principal com listagem de pontos turísticos e filtros
* **`/statistics/`**: Página de estatísticas
* **`/api/types-for-city/`**: Endpoint AJAX que retorna os tipos disponíveis para uma cidade específica

### Sistema de Filtros em Cascata

O sistema de filtros em cascata funciona através de uma combinação de Django e JavaScript:

1. Quando uma cidade é selecionada, um pedido AJAX é enviado para `/api/types-for-city/`
2. O backend filtra os tipos que existem naquela cidade específica
3. O frontend atualiza o dropdown de tipos com as opções retornadas
4. Os filtros mantêm seu estado durante a navegação de páginas

## 🎯 Comandos Disponíveis

* `import_spots`: Importa pontos turísticos de um arquivo CSV
  * Opção `--clear`: Limpa os dados existentes antes de importar (opcional)
  * Ignora registros duplicados por default
* `populate_city_types`: Popula a tabela de tipos por cidade
* `list_cities_types`: Lista todas as cidades e seus respectivos tipos

## 🔍 Como Usar

1. Acesse a página inicial em `http://localhost:8000/` (local) ou `https://turismo-interior.onrender.com/` (produção)
2. Use os filtros para encontrar pontos turísticos:  
   * Selecione uma cidade  
   * Observe como o dropdown de tipos é atualizado automaticamente
   * Escolha um tipo para refinar sua busca
3. Navegue entre as páginas usando a paginação
4. Clique em "Ver no Maps" para ver a localização no Google Maps
5. Acesse as estatísticas em `/statistics/`

## 📝 Estrutura do CSV

O arquivo CSV deve conter as seguintes colunas:
- Nome
- Endereço
- Cidade
- Avaliação
- Tipos (separados por vírgula)
- Latitude
- Longitude
- Place_ID

## ⚠️ Solução de Problemas

### Filtros não funcionam corretamente
- Verifique se o JavaScript está habilitado no navegador
- Inspecione o console do navegador para erros
- O endpoint `/api/types-for-city/` deve retornar um array JSON com os tipos disponíveis
- A consulta SQL usa `Type.objects.filter(touristspot__city=city)` para obter os tipos por cidade

### Erro no Deploy
- Verifique os logs no painel do Render.com
- Confirme que os caminhos no `render.yaml` estão corretos
- O comando `import_spots` agora ignora registros duplicados automaticamente

### Dados Faltantes
- Certifique-se de usar o CSV correto com todos os campos necessários
- Verifique as permissões de acesso ao arquivo CSV
- Os tipos devem estar separados por vírgula no campo "Tipos"

## 🔄 Atualizações Recentes

* **Filtros em Cascata**: Correção do sistema de filtros para mostrar corretamente os tipos disponíveis por cidade
* **Importação Robusta**: Melhoria no comando `import_spots` para lidar com registros duplicados
* **Interface Otimizada**: Adição de feedback visual durante o carregamento dos filtros

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

