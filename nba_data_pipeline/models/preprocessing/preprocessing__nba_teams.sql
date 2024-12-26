{{
    config(
        materialised="table"
    )
}}

SELECT
    TEAM_ID AS team_id,
    CONCAT(CITY, " ", NICKNAME) AS team_name,
    YEARFOUNDED AS year_founded,
    CITY AS city,
    ARENA AS arena_name,
    ARENACAPACITY AS arena_capacity,
    OWNER AS team_owner,
    GENERALMANAGER AS team_general_manager,
    HEADCOACH AS team_head_coach,
    DLEAGUEAFFILIATION AS d_league_team_name,
    MAX_YEAR AS max_year
    
FROM `{{ project() }}.nba_pipeline_dataset.teams`

