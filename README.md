# Virtual Manager

Simple portfolio application for virtual machines administration (may be used like a wrapper over VMWare)

## Build Setup

Run:
```bash
$ docker pull postgres
$ docker run -d \
    -p 5432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=postgres \
    --name postgres \
    postgres
$ docker-compose up -d
```
Then:   
http://127.0.0.1:8080
