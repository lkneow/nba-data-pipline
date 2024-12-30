{{
    config(
        materialised="table"
    )
}}

{#-
/*There are duplicates in the source due to different rounding in PCT columns. Removing it here
    distinct doesn't work since some data is different. Using qualify
*/ -#}
SELECT
    GAME_ID AS game_id,
    TEAM_ID AS team_id,
    TEAM_ABBREVIATION AS team_abbreviation,
    PLAYER_ID AS player_id,
    PLAYER_NAME AS player_name,
    NICKNAME AS nickname,
    START_POSITION AS start_position,
    COMMENT AS dnp_comment,
    CAST(FGM AS INT) AS field_goals_made,
    CAST(FGA AS INT) AS field_goals_attempted,
    ROUND(FG_PCT, 3) AS field_goal_percentage,
    CAST(FG3M AS INT) AS three_pointers_made,
    CAST(FG3A AS INT) AS three_pointers_attempted,
    ROUND(FG3_PCT, 3) AS three_point_percentage,
    CAST(FTM AS INT) AS free_throws_made,
    CAST(FTA AS INT) AS free_throws_attempted,
    ROUND(FT_PCT, 3) AS free_throw_percentage,
    CAST(OREB AS INT) AS offensive_rebounds,
    CAST(DREB AS INT) AS defensive_rebounds,
    CAST(REB AS INT) AS total_rebounds,
    CAST(AST AS INT) AS assists,
    CAST(STL AS INT) AS steals,
    CAST(BLK AS INT) AS blocks,
    CAST(`TO` AS INT) AS turnovers,
    CAST(PF AS INT) AS personal_fouls,
    CAST(PTS AS INT) AS points,
    CAST(PLUS_MINUS AS INT) AS plus_minus

FROM {{ source('nba_pipeline_dataset_raw', 'games_details') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY
        GAME_ID,
        TEAM_ID,
        PLAYER_ID
) = 1
