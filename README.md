# Portal de Turismo do Interior de São Paulo

Um portal web desenvolvido em Django para explorar pontos turísticos do interior de São Paulo, com filtros dinâmicos, estatísticas e integração com Google Maps.

## 🚀 Funcionalidades

* **Listagem de Pontos Turísticos**  
   * Visualização em cards com informações detalhadas  
   * Paginação (9 itens por página)  
   * Filtros dinâmicos por cidade e tipo  
   * Integração com Google Maps
* **Filtros Inteligentes**  
   * Filtro por cidade com suporte a variações de nome (ex: "Cidade" ou "Cidade, SP")
   * Busca case-insensitive para maior flexibilidade
   * Filtro de tipos que se atualiza automaticamente baseado na cidade selecionada
   * Sistema de fallback para busca de tipos quando não há correspondência exata
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

## 🔍 Sistema de Filtros

O sistema de filtros foi aprimorado para lidar com diversos cenários e melhorar a experiência do usuário:

### Filtro por Cidade
* Suporta cidades com ou sem o sufixo ", SP"
* Busca case-insensitive usando `icontains`
* Mantém a seleção durante a navegação entre páginas

### Filtro por Tipo
* Atualização dinâmica baseada na cidade selecionada
* Sistema de fallback para busca mais flexível:
  1. Tenta correspondência exata com a cidade
  2. Se não encontrar, remove o sufixo ", SP"
  3. Se ainda não encontrar, usa apenas a primeira palavra da cidade
* Evita duplicação de tipos no dropdown
* Mantém a seleção ao navegar entre páginas

### Otimizações de Performance
* Debounce nas chamadas de API
* Carregamento seletivo de tipos
* Cache de consultas usando `select_related` e `prefetch_related`

## 🔄 Últimas Atualizações

* **Nova Tabela CityTypes**: Implementação de tabela otimizada para armazenar tipos por cidade
* **Sistema de Cache de Tipos**: Melhoria na performance da busca de tipos por cidade
* **Atualização Automática**: Sistema atualiza automaticamente os tipos quando necessário
* **Melhor Diagnóstico**: Logs detalhados para facilitar a identificação de problemas
* **Otimização de Consultas**: Índices adicionados para melhor performance

## 🗃️ Estrutura do Banco de Dados

### Tabelas Principais
* **TouristSpot**: Armazena os pontos turísticos
* **Type**: Armazena os tipos de pontos turísticos
* **CityTypes**: Nova tabela que mantém um cache dos tipos por cidade

### Índices e Otimizações
* Índice na coluna `city` do TouristSpot
* Índices compostos na tabela CityTypes
* Constraint unique para evitar duplicatas

## 🔧 Comandos de Manutenção

* **import_spots**: Importa pontos turísticos do CSV
  ```bash
  python manage.py import_spots caminho/do/arquivo.csv
  ```

* **update_city_types**: Atualiza a tabela de tipos por cidade
  ```bash
  python manage.py update_city_types
  ```

## ⚠️ Solução de Problemas

### Tipos não aparecem para uma cidade
1. Verifique se há pontos turísticos cadastrados para a cidade
2. Execute o comando `update_city_types` para reconstruir o cache
3. Verifique os logs para mais detalhes do problema

### Erro na importação de dados
1. Verifique se o arquivo CSV está no formato correto
2. Execute a importação com `--verbosity 2` para mais detalhes
3. Após a importação, execute `update_city_types`

### Performance dos Filtros
* A tabela CityTypes mantém um cache dos tipos por cidade
* As consultas são otimizadas com índices
* O sistema atualiza automaticamente o cache quando necessário

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

