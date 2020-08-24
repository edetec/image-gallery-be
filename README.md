# image-gallery-be
Para execupar o projeto é preciso instalar o Python 3.8 e o Pipenv

## Configuração do banco de dados
A configuração padrão utiliza o sqlite porém, opcionamente é possível definir a variável de ambiente mostrada abaixo
```
 SQLALCHEMY_DATABASE_URI=mysql://username:password@server/db
```

## Dependências
Para instalar as dependências, entre no diretório do projeto e execute os comandos:
```
 pipenv install
```

## Executar
Para iniciar o servidor:
```
 pipenv run python wsgi.py
```

## Testes
Para executar os testes:
```
 pipenv run pytest
```