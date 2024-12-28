# Airflow setup

Following the no frills setup [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2022/week_3_data_warehouse/airflow/2_setup_nofrills.md)
- revelant links
    - https://www.clearpeaks.com/creating-a-local-airflow-environment-using-docker-compose/
    - https://datatalks.club/blog/how-to-setup-lightweight-local-version-for-airflow.html

## Notes
- `AIRFLOW_UID` is set to 1000
- will have to run `mkdir -p ./dags ./logs ./plugins`
- use [`.env_example`](.env_example) to make a `.env`
- Note the airflow and gcloud sdk version in [Dockerfile](Dockerfile)
    - pip moved to after AIRFLOW_UID since it can't run with root?
- Note the location of creds in [docker-compose.yaml](docker-compose.yaml)

## Credentials
There is a creds folder with service account credentials as google_credentials.json

## References
astronomer cosmos documentation: https://astronomer.github.io/astronomer-cosmos/getting_started/index.html

elt bigquery dbt: https://www.astronomer.io/docs/learn/reference-architecture-elt-bigquery-dbt/

astronomer cosmos simple dag example: https://github.com/astronomer/cosmos-demo/blob/main/dags/basic/simple_dag.py
