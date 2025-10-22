# Youtube ELT: Data Engineering


### Some commands to interact with airflow
```shell
docker ps
```
```shell
docker exec -it airflow-scheduler bash
```
```shell
cd data
```
```shell
ls
```
```shell
airflow --help
```
```shell
airflow info
```
```shell
airflow cheat-sheet -v
```

## spin up docker with builds
```shell
docker compose up -d --build
```

```shell
docker exec -it airflow-webserver bash
env | grep AIRFLOW_VAR
```

## Interact with database from docker psql
```shell
docker exec -it postgres psql -U yt_api_user -d elt_db
```

## Building new image
```shell
docker build -t bgnti/youtube_api_elt:1.0.1 .
dcoker compose pull
docker-compose up -d --force-recreate
```

## test soda connection
```shell
dataquality test-connection -d pg_datasource -c /opt/airflow/include/dataquality/configuration.yml -V
```

## running soda tests
```shell
dataquality scan -d pg_datasource -c /opt/airflow/include/dataquality/configuration.yml -v SCHEMA=core  /opt/airflow/include/dataquality/checks.yml
```

## running tests
```shell
pytest -v tests/unit_test.py -k test_api_key
```

```shell
airlfow dags test produce_json
```