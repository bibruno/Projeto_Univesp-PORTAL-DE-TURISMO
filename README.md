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
   * Busca flexível e inteligente de tipos por cidade
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

6. Inicie o servidor:
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
│   │   │   │       ├── list.html
│   │   │   │       └── statistics.html
│   │   │   ├── management/
│   │   │   │   └── commands/
│   │   │   │       ├── import_spots.py
│   │   │   │       └── populate_city_types.py (stub para compatibilidade)
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
* **City**: Representa uma cidade com seu nome único
* **CityType**: (Legado/Não utilizado) Mantido apenas para compatibilidade com comandos antigos

### API e Endpoints

* **`/`**: Página principal com listagem de pontos turísticos e filtros
* **`/statistics/`**: Página de estatísticas
* **`/api/types-for-city/`**: Endpoint AJAX que retorna os tipos disponíveis para uma cidade específica

### Sistema de Filtros em Cascata

O sistema de filtros em cascata funciona através de uma combinação de Django e JavaScript:

1. Quando uma cidade é selecionada, um pedido AJAX é enviado para `/api/types-for-city/`
2. O backend executa uma consulta de tipos com estratégias flexíveis:
   - Primeiro tenta uma correspondência exata (`Type.objects.filter(touristspot__city=city)`)
   - Se não encontrar resultados, tenta uma busca parcial do nome da cidade (`city__contains=nome_da_cidade`)
   - Lida com formatos como "Cidade, SP" removendo sufixos se necessário
3. O frontend atualiza o dropdown de tipos com as opções retornadas
4. Um painel de debug na interface permite visualizar as requisições e respostas em tempo real
5. Os filtros mantêm seu estado durante a navegação entre páginas

## 🎯 Comandos Disponíveis

* `import_spots`: Importa pontos turísticos de um arquivo CSV
  * Opção `--clear`: Limpa os dados existentes antes de importar (opcional)
  * Ignora registros duplicados por default
* `populate_city_types`: (Legado/Não utilizado) Mantido como stub para compatibilidade com deployments existentes

## 🔍 Como Usar

1. Acesse a página inicial em `http://localhost:8000/` (local) ou `https://turismo-interior.onrender.com/` (produção)
2. Use os filtros para encontrar pontos turísticos:  
   * Selecione uma cidade  
   * Observe como o dropdown de tipos é atualizado automaticamente
   * Escolha um tipo para refinar sua busca
3. Para ativar o modo de debug, utilize o botão "Mostrar/Esconder Debug" que aparece na área de filtros
4. Navegue entre as páginas usando a paginação
5. Clique em "Ver no Maps" para ver a localização no Google Maps
6. Acesse as estatísticas em `/statistics/`

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
- **Verificação básica**: Certifique-se que o JavaScript está habilitado no navegador
- **Depuração**: Clique no botão "Mostrar/Esconder Debug" para ver logs detalhados
- **Chamada API**: Verifique se a chamada para `/api/types-for-city/` está retornando status 200
- **Formato de cidades**: A busca agora é flexível e suporta formatos como "Cidade, SP" ou apenas "Cidade"
- **Console do navegador**: Inspecione o console (F12) para erros de JavaScript
- **Logs do servidor**: Verifique o terminal do servidor Django para erros ou mensagens de debug

### Erro no Deploy no Render.com
- **Logs de deploy**: Verifique os logs completos no painel do Render.com
- **Compatibilidade de comandos**: O comando `populate_city_types` foi mantido como stub para compatibilidade
- **Build cache**: Se necessário, use "Clear build cache & deploy" no painel do Render
- **GitHub sincronizado**: Certifique-se que todas as alterações foram enviadas para o GitHub com `git push`

### Dados Faltantes ou Incorretos
- **Formato do CSV**: Certifique-se de usar o formato correto com todos os campos necessários
- **Importação com debug**: Execute `python manage.py import_spots --verbosity 2 caminho/do/arquivo.csv` para logs detalhados
- **Consulta direta**: Use o Django shell para verificar se os dados foram importados corretamente

## 🔄 Atualizações Recentes

* **Busca Inteligente de Tipos**: Implementação de um algoritmo mais flexível para busca de tipos por cidade
* **Painel de Debug**: Adição de um painel interativo para debug das chamadas AJAX e respostas
* **Análise de Erros Avançada**: Inclusão de logs detalhados para diagnóstico de problemas
* **Refatoração do Backend**: Remoção de dependência do modelo CityType em favor de consultas dinâmicas
* **Compatibilidade Render.com**: Garantia de compatibilidade com o sistema de deploy automático

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

