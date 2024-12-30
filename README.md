# nba-data-pipline
NBA data pipeline practice

## Data
Taken from https://www.kaggle.com/datasets/nathanlauga/nba-games

## What I did

Python version: 3.12.1
- This is the version on github codespace

Set up python virtual environment

```bash
python -m venv .venv
pip install -r requirements.txt
```

Install [gcloud cli](https://cloud.google.com/sdk/docs/install#linux)
- Steps are in `install-google-cli.sh`
- will have to `chmod +x install-google-cli.sh` to run it
- will have to do `gcloud auth application-default login`
`
Install [terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli#install-terraform)
- other instructions will be in a README.md under the terraform folder
- I have a `.env` file thats for airflow, but terraform seems to use the `GOOGLE_APPLICATION_CREDENTIALS` from there

Install [docker](https://docs.docker.com/engine/install/ubuntu/), [docker compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository)
- These come preinstalled in github codespaces. Install if required
- relevant commands
    ```bash
    docker compose up
    docker compose down --rmi all
    ```

Set up dbt with [dbt init](https://docs.getdbt.com/reference/commands/init)
- model folder moved to [airflow/dags](/airflow/dags) to use [astronomer-cosmos](https://astronomer.github.io/astronomer-cosmos/)
- Moved [profiles.yml](/airflow/dags/nba_data_pipeline/profiles.yml) to the dbt project folder. was originally under `~/.dbt`
- added `flags: send_anonymous_usage_stats: False`

Set up airflow
- [README](/airflow/README.md) in the folder itself

## The DAGS

### [data_ingestion_gcp.py](/airflow/dags/data_ingestion_gcp.py)
![load_to_gcs_dag](/img/load_to_gcs_dag.PNG)

### [nba_data_pipeline_dbt_dag](/airflow/dags/nba_data_pipeline_dbt_dag.py)
![nba_data_pipeline_dbt_dag](/img/nba_data_pipeline_dbt_dag.PNG)

## dbt lineage
![dbt_lineage](/img/dbt_lineage.PNG)

## [nba_data_pipeline dbt model](/airflow/dags/nba_data_pipeline/) directory tree

```bash
├── analyses
├── macros
│   ├── dataset_raw.sql
│   └── project.sql
├── models
│   ├── core
│   │   ├── core__nba_game_stats.sql
│   │   └── core__nba_game_stats.yml
│   ├── preprocessing
│   │   ├── preprocessing__nba_games.sql
│   │   ├── preprocessing__nba_games.yml
│   │   ├── preprocessing__nba_players.sql
│   │   ├── preprocessing__nba_players.yml
│   │   ├── preprocessing__nba_players_game_stats.sql
│   │   ├── preprocessing__nba_players_game_stats.yml
│   │   ├── preprocessing__nba_team_standings.sql
│   │   ├── preprocessing__nba_team_standings.yml
│   │   ├── preprocessing__nba_teams.sql
│   │   └── preprocessing__nba_teams.yml
│   └── sources.yml
├── seeds
├── snapshots
├── tests
├── dbt_project.yml
└── profiles.yml
```
