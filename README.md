# Portal de Turismo do Interior de São Paulo

Este projeto é um portal de turismo que lista pontos turísticos do interior do estado de São Paulo, com informações detalhadas sobre cada local, incluindo avaliações, tipos de estabelecimento e localização.

## Funcionalidades

- Listagem de pontos turísticos com paginação
- Filtros por cidade e tipo de estabelecimento
- Estatísticas gerais sobre os pontos turísticos
- Integração com Google Maps
- Interface responsiva e moderna

## Requisitos

- Python 3.8 ou superior
- Django 5.2
- Bootstrap 5.3
- SQLite3

## Instalação

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
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Importe os dados dos pontos turísticos:
```bash
python import_data_simple.py
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

7. Acesse a aplicação em http://localhost:8000/

## Estrutura do Projeto

```
Projeto_Univesp-PORTAL-DE-TURISMO/
├── turismo_interior/          # Projeto Django principal
│   ├── pontos_turisticos/     # App de pontos turísticos
│   │   ├── migrations/        # Migrações do banco de dados
│   │   ├── templates/         # Templates HTML
│   │   ├── models.py          # Modelos de dados
│   │   ├── views.py           # Views da aplicação
│   │   └── urls.py            # URLs da aplicação
│   ├── settings.py            # Configurações do projeto
│   └── urls.py                # URLs do projeto
├── Banco/                     # Dados dos pontos turísticos
├── import_data_simple.py      # Script de importação
├── manage.py                  # Script de gerenciamento Django
├── requirements.txt           # Dependências do projeto
└── README.md                  # Este arquivo
```

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 