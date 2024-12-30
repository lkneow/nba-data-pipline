{{
    config(
        materialised = 'table'
    )
}}

SELECT
    game_stats.game_id,
    COALESCE(games_home.game_date_est, games_away.game_date_est) AS game_date_est,
    game_stats.team_id,
    teams.team_name,
    games_home.team_id_home IS NOT NULL AS is_home_team,
    COALESCE(games_home.home_team_wins, games_away.home_team_wins) AS is_win,
    SUM(game_stats.field_goals_made) AS total_field_goals_made,
    SUM(game_stats.field_goals_attempted) AS total_field_goals_attempted,
    SUM(game_stats.three_pointers_made) AS total_three_pointers_made,
    SUM(game_stats.three_pointers_attempted) AS total_three_pointers_attempted,

    SUM(game_stats.free_throws_made) AS total_free_throws_made,
    SUM(game_stats.free_throws_attempted) AS total_free_throws_attempted,

    SUM(game_stats.offensive_rebounds) AS total_offensive_rebounds,
    SUM(game_stats.defensive_rebounds) AS total_defensive_rebounds,
    SUM(game_stats.total_rebounds) AS total_total_rebounds,
    SUM(game_stats.assists) AS total_assists,
    SUM(game_stats.steals) AS total_steals,
    SUM(game_stats.blocks) AS total_blocks,
    SUM(game_stats.turnovers) AS total_turnovers,
    SUM(game_stats.personal_fouls) AS total_personal_fouls

FROM {{ ref('preprocessing__nba_players_game_stats') }} AS game_stats
LEFT JOIN {{ ref('preprocessing__nba_games') }} AS games_home
       ON game_stats.game_id = games_home.game_id
      AND game_stats.team_id = games_home.team_id_home
LEFT JOIN {{ ref('preprocessing__nba_games') }} AS games_away
       ON game_stats.game_id = games_away.game_id
      AND game_stats.team_id = games_away.team_id_away
LEFT JOIN {{ ref('preprocessing__nba_teams') }} AS teams
       ON game_stats.team_id = teams.team_id
GROUP BY ALL
