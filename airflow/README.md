# Airflow setup

Following the no frills setup [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2022/week_3_data_warehouse/airflow/2_setup_nofrills.md)
- revelant links
    - https://www.clearpeaks.com/creating-a-local-airflow-environment-using-docker-compose/
    - https://datatalks.club/blog/how-to-setup-lightweight-local-version-for-airflow.html

## Notes
- Airflow user and password will be `admin`, `admin`
- `AIRFLOW_UID` is set to 1000
- will have to run `mkdir -p ./dags ./logs ./plugins`
- use [`.env_example`](.env_example) to make a `.env`
- Note the airflow and gcloud sdk version in [Dockerfile](Dockerfile)
    - pip moved to after AIRFLOW_UID since it can't run with root?
- Note the location of creds in [docker-compose.yaml](docker-compose.yaml)
- dbt docs are hosted following the [instructions shown](https://astronomer.github.io/astronomer-cosmos/configuration/hosting-docs.html) on the astronmer-cosmos documentation page

## Commands

To start the local airflow instance
```bash
docker compose up
```

To shut down the airflow instance and remove all related images
```bash
docker compose down --rmi all
```

To run tests
```bash
docker compose up -d
docker exec -it nba-pipeline-scheduler-1 pytest -v
```

## References
astronomer cosmos documentation: https://astronomer.github.io/astronomer-cosmos/getting_started/index.html

elt bigquery dbt: https://www.astronomer.io/docs/learn/reference-architecture-elt-bigquery-dbt/

astronomer cosmos simple dag example: https://github.com/astronomer/cosmos-demo/blob/main/dags/basic/simple_dag.py

## Issues

astronomer-cosmos 1.8.0 has a [bug](https://github.com/astronomer/astronomer-cosmos/issues/1420)
- issue with `DbtDocsGCSOperator`
