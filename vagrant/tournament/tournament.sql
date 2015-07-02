CREATE DATABASE tournament;
\c tournament;

DROP TABLE players, results CASCADE;

CREATE TABLE players (
        player_id serial PRIMARY KEY,
        name varchar (25) NOT NULL
);


CREATE TABLE results (
        match_id serial PRIMARY KEY,
        winner integer REFERENCES players(player_id) NOT NULL,
        loser integer REFERENCES players(player_id) NOT NULL
);


CREATE VIEW standings AS
SELECT players.player_id, players.name,
(SELECT count(results.winner) 
    FROM results 
    WHERE players.player_id = results.winner) 
    AS total_wins,
(SELECT count(results.match_id) 
    FROM results 
    WHERE players.player_id = results.winner
    OR players.player_id = results.loser) 
    AS total_matches
FROM players
ORDER BY total_wins DESC, total_matches DESC;











