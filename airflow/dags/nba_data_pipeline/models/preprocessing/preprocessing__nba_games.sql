{{
    config(
        materialised="table"
    )
}}

SELECT
    GAME_ID AS game_id,
    GAME_DATE_EST AS game_date_est,
    GAME_STATUS_TEXT AS game_status,
    SEASON AS game_season,
    HOME_TEAM_ID AS team_id_home,
    PTS_home AS points_home,
    ROUND(FG_PCT_home, 3) AS field_goal_pct_home,
    ROUND(FT_PCT_home, 3) AS free_throw_pct_home,
    ROUND(FG3_PCT_home, 3) AS three_point_fg_pct_home,
    AST_home AS assists_home,
    REB_home AS rebounds_home,
    TEAM_ID_away AS team_id_away,
    PTS_away AS points_away,
    ROUND(FG_PCT_away, 3) AS field_goal_pct_away,
    ROUND(FT_PCT_away, 3) AS free_throw_pct_away,
    ROUND(FG3_PCT_away, 3) AS three_point_fg_pct_away,
    AST_away AS assists_away,
    REB_away AS rebounds_away,
    HOME_TEAM_WINS = 1 AS home_team_wins
FROM {{ source('nba_pipeline_dataset_raw', 'games') }}
