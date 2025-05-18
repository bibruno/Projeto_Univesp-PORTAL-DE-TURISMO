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
* **Frontend**  
   * HTML5  
   * CSS3  
   * JavaScript  
   * Bootstrap 5.3  
   * Bootstrap Icons

## 📋 Pré-requisitos

* Python 3.x
* pip (gerenciador de pacotes Python)
* Git (opcional)

## 🔧 Instalação

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
python manage.py import_spots ../Banco/pontos_turisticos_traduzido.csv
```

6. Popule a tabela de tipos por cidade:
```bash
python manage.py populate_city_types
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## 📊 Estrutura do Projeto

```
Projeto_Univesp-PORTAL-DE-TURISMO/
├── turismo_interior/
│   ├── turismo_interior/
│   │   ├── pontos_turisticos/
│   │   │   ├── migrations/
│   │   │   ├── templates/
│   │   │   │   ├── base.html
│   │   │   │   ├── list.html
│   │   │   │   └── statistics.html
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
│   └── Banco/
│       └── pontos_turisticos_traduzido.csv
├── render.yaml
└── README.md
```

## 🎯 Comandos Disponíveis

* `import_spots`: Importa pontos turísticos de um arquivo CSV
* `populate_city_types`: Popula a tabela de tipos por cidade
* `list_cities_types`: Lista todas as cidades e seus respectivos tipos

## 🔍 Como Usar

1. Acesse a página inicial em `http://localhost:8000/`
2. Use os filtros para encontrar pontos turísticos:  
   * Selecione uma cidade  
   * Escolha um tipo (a lista se atualiza baseado na cidade)
3. Navegue entre as páginas usando a paginação
4. Clique em "Ver no Maps" para ver a localização no Google Maps
5. Acesse as estatísticas em `http://localhost:8000/statistics/`

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

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

