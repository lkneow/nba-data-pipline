{{
    config(
        materialised="table"
    )
}}

SELECT
    TEAM_ID AS team_id,
    SEASON_ID AS season_id,
    STANDINGSDATE AS standings_date,
    CONFERENCE AS conference,
    CAST(G AS INT) AS games_played,
    CAST(W AS INT) AS wins,
    CAST(L AS INT) AS losses,
    ROUND(W_PCT, 3) AS win_percentage,
    HOME_RECORD AS home_record,
    CAST(SPLIT(HOME_RECORD, '-')[OFFSET(0)] AS INT) AS home_wins,
    CAST(SPLIT(HOME_RECORD, '-')[OFFSET(1)] AS INT) AS home_losses,
    ROUND(
        CAST(SPLIT(HOME_RECORD, '-')[OFFSET(0)] AS FLOAT) /
        (CAST(SPLIT(HOME_RECORD, '-')[OFFSET(0)] AS FLOAT) + CAST(SPLIT(HOME_RECORD, '-')[OFFSET(1)] AS FLOAT)),
        3
    ) AS home_win_percentage
    ROAD_RECORD AS road_record,
    CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(0)] AS INT) AS road_wins,
    CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(1)] AS INT) AS road_losses,
    ROUND(
        CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(0)] AS FLOAT) /
        (CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(0)] AS FLOAT) + CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(1)] AS FLOAT)),
        3
    ) AS road_win_percentage

FROM `{{ project() }}.nba_pipeline_dataset.ranking`
