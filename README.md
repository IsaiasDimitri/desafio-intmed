# Instruções de Instalação

### Requisitos
Docker e docker-composer
Python 3.6+

```
git clone https://github.com/IsaiasDimitri/desafio-intmed.git desafio
cd desafio
docker-compose build
docker-compose up
```
Opcionalmente, voce pode criar um superuser. Somente com ele voce pode fazer todas as listagens
```
docker-compose rm -rm api python manage.py createsuperuser
```

### API endpoints

- base_url = localhost:8000/

| Url | Descrição |
|-----|---------------|
| users/ |   listagem e cadastro de usuarios |
|especialidades/ | listagem e cadastro de especialidades|
|medicos/ | listagem e cadastro de medicos|
|agendas/ | listagem e cadastro de agendas|
|consultas/ | listagem e cadastro de consultas|
|api-token-auth/ | receber token para uso nas requests|

