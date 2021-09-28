# Instruções de Instalação

### Requisitos
Docker e docker-composer
Python 3.6+

```
git clone https://github.com/IsaiasDimitri/desafio-intmed.git desafio
cd desafio
```
Para evitar erros, confira se o arquivo 'docker-entrypoint.sh' está no formato LF, e se necessário modifique-o.

```
docker-compose build
docker-compose up
```

Por padrão, você já pode capturar um token com o superusuário padrão de acesso administrador/admin123.  
Com esse usuário você será capaz de criar e listar nas URL's que usuários normais não podem.

### API endpoints

O arquivo collection.json contem todas as requisições e exemplos de consulta/cadastro.  
Ele pode ser importado pelo Insomnia, ou pelo Postman.

- base_url = localhost:8000/

| Url | Descrição |
|-----|---------------|
| users/ |   listagem e cadastro de usuarios |
|especialidades/ | listagem e cadastro de especialidades|
|medicos/ | listagem e cadastro de medicos|
|agendas/ | listagem e cadastro de agendas|
|consultas/ | listagem e cadastro de consultas|
|api-token-auth/ | receber token para uso nas requests|

