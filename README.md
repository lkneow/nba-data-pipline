# nba-data-pipline
NBA data pipeline practice

# Data
Taken from https://www.kaggle.com/datasets/nathanlauga/nba-games

# What I did

Python version: 3.12.1
- This is the version on github codespace

Set up python virtual environment

```
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
    ``` 
    docker compose up
    docker compose down --rmi all
    ```

Set up dbt with [dbt init](https://docs.getdbt.com/reference/commands/init)
- Moved [profiles.yml](nba_data_pipeline/profiles.yml) to the dbt project folder
- added `flags: send_anonymous_usage_stats: False`