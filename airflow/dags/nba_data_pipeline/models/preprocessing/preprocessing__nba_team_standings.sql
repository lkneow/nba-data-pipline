{{
    config(
        materialised="table"
    )
}}

{#- /*There are duplicates in the source due to different rounding in PCT columns. Removing it here*/ -#}
WITH ranking_clean AS (
    SELECT
        TEAM_ID,
        SEASON_ID,
        STANDINGSDATE,
        CONFERENCE,
        G,
        W,
        L,
        HOME_RECORD,
        ROAD_RECORD
    FROM {{ source('nba_pipeline_dataset_raw', 'games_details') }}
)

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
        SAFE_DIVIDE(
            CAST(SPLIT(HOME_RECORD, '-')[OFFSET(0)] AS NUMERIC),
            (CAST(SPLIT(HOME_RECORD, '-')[OFFSET(0)] AS NUMERIC) + CAST(SPLIT(HOME_RECORD, '-')[OFFSET(1)] AS NUMERIC))
        ),
        3
    ) AS home_win_percentage,
    ROAD_RECORD AS road_record,
    CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(0)] AS INT) AS road_wins,
    CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(1)] AS INT) AS road_losses,
    ROUND(
        SAFE_DIVIDE(
            CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(0)] AS NUMERIC),
            (CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(0)] AS NUMERIC) + CAST(SPLIT(ROAD_RECORD, '-')[OFFSET(1)] AS NUMERIC))
        ),
        3
    ) AS road_win_percentage

FROM ranking_clean
