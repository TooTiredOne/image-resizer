# Image Resizer

## Description:
    A simple image-resizing service api with Redis Queue
    
    swagger documentation is available on 0.0.0.0:8000/docs


## Run app:
    docker-compose up

## Create venv:
    make venv

## Run tests:
    docker-compose run app make test

## Run linters:
    make lint

## Run formatters:
    make format


## Docker
    docker-compose build app
    docker-compose run --rm app make test
    docker-compose up
    docker-compose up -d

