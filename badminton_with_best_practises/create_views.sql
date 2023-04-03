CREATE OR REPLACE VIEW games_view
AS SELECT g.id AS game_id,
    s.club_id,
    s.season_id,
    g.session_id,
    g.team1_id AS team_1,
    g.team2_id AS team_2,
    g.team1_score AS team_1_score,
    g.team2_score AS team_2_score,
    g.winner_team_id AS winning_team,
    array_agg(DISTINCT tp1.player_id) AS team_1_player_ids,
    array_agg(DISTINCT tp2.player_id) AS team_2_player_ids,
    array_agg(DISTINCT p1.name) AS team_1_player_names,
    array_agg(DISTINCT p2.name) AS team_2_player_names,
    game_start_time,
    game_end_time
FROM games g
    JOIN sessions s ON g.session_id = s.id
    JOIN teams t1 ON g.team1_id = t1.id
    JOIN teams t2 ON g.team2_id = t2.id
    JOIN teams_players tp1 ON t1.id = tp1.team_id
    JOIN teams_players tp2 ON t2.id = tp2.team_id
    JOIN players p1 ON tp1.player_id = p1.id
    JOIN players p2 ON tp2.player_id = p2.id
GROUP BY g.id, g.session_id, s.season_id, s.club_id, g.team1_id, g.team2_id, g.team1_score, g.team2_score, g.winner_team_id;


CREATE OR REPLACE VIEW player_stats_by_session AS
SELECT
    sp.session_id,
    sp.player_id,
    p.name AS player_name,
    sp.played AS games_played,
    sp.won,
    sp.played - sp.won - sp.draw AS lost,
    round((sp.won * 100.0) / sp.played, 2) AS win_percentage,
    round(EXTRACT(EPOCH FROM (NOW() - g.game_end_time)) / 60) AS minutes_since_last_game,
    DENSE_RANK() OVER (PARTITION BY sp.session_id ORDER BY sp.win_percentage DESC, sp.played DESC) AS session_rank
FROM
    sessions_players sp
JOIN players p ON p.id = sp.player_id
LEFT JOIN (
    SELECT
        gv.session_id,
        unnest(array_cat(gv.team_1_player_ids, gv.team_2_player_ids)) AS player_id,
        MAX(gv.game_end_time) AS game_end_time
    FROM
        games_view gv
    WHERE
        gv.game_end_time IS NOT NULL
    GROUP BY
        gv.session_id,
        unnest(array_cat(gv.team_1_player_ids, gv.team_2_player_ids))
) g ON g.session_id = sp.session_id AND g.player_id = sp.player_id;

CREATE VIEW season_player_stats AS
SELECT
    s.season_id,
    sp.player_id,
    p.name,
    SUM(sp.played) AS played,
    SUM(sp.won) AS won,
    SUM(sp.draw) AS draw,
    ROUND(100.0 * SUM(sp.won) / SUM(sp.played), 2) AS win_percentage,
    RANK() OVER (PARTITION BY s.season_id ORDER BY ROUND(100.0 * SUM(sp.won) / SUM(sp.played), 2) DESC) AS season_rank
FROM
    sessions_players sp
JOIN players p ON sp.player_id = p.id
JOIN sessions s ON sp.session_id = s.id
GROUP BY
    s.season_id,
    sp.player_id,
    p.name;

CREATE VIEW club_player_stats AS
SELECT
    s.club_id,
    sp.player_id,
    p.name,
    SUM(sp.played) AS played,
    SUM(sp.won) AS won,
    SUM(sp.draw) AS draw,
    ROUND(100.0 * SUM(sp.won) / SUM(sp.played), 2) AS win_percentage,
    RANK() OVER (PARTITION BY s.club_id ORDER BY ROUND(100.0 * SUM(sp.won) / SUM(sp.played), 2) DESC) AS club_rank
FROM
    sessions_players sp
JOIN players p ON sp.player_id = p.id
JOIN sessions s ON sp.session_id = s.id
GROUP BY
    s.club_id,
    sp.player_id,
    p.name;
