{{
    config(
        materialised="table"
    )
}}

SELECT
    PLAYER_ID AS player_id,
    PLAYER_NAME AS player_name,
    TEAM_ID AS team_id,
    SEASON AS season_year
FROM `{{ project() }}.nba_pipeline_dataset.players`
WHERE PLAYER_ID IS NOT NULL
