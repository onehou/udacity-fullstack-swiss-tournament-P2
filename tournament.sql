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

INSERT INTO players (player_id, name) VALUES
        (default, 'Moe'), (default, 'Larry'),
        (default, 'Curly'), (default, 'Shemp'),
        (default, 'Curly Joe'), (default, 'Joe Curly');

INSERT INTO results (match_id, winner, loser) VALUES
        (default, 1, 2),
        (default, 3, 2),
        (default, 1, 4);


CREATE VIEW wins AS
SELECT players.player_id, players.name, count(results.winner) as total_winners
FROM  players
LEFT JOIN results
ON players.player_id = results.winner
GROUP BY player_id
ORDER BY total_winners desc;


CREATE VIEW standings AS
SELECT players.player_id, players.name,
(SELECT count(results.winner) FROM results WHERE players.player_id = results.winner) AS total_wins,
(SELECT count(results.winner) FROM results WHERE players.player_id = results.winner
  OR players.player_id = results.loser) AS total_matches
FROM players
ORDER BY total_wins desc, total_matches desc;


