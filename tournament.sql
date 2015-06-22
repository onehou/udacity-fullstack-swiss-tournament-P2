CREATE DATABASE tournament;

\c tournament;

DROP TABLE players, matches, results CASCADE;

CREATE TABLE players (
        player_id serial PRIMARY KEY,
        name varchar (25) NOT NULL
);


CREATE TABLE matches (
        match_id serial PRIMARY KEY NOT NULL,
        match_date date NOT NULL,
        player1 integer REFERENCES players(player_id) NOT NULL,
        player2 integer REFERENCES players(player_id) NOT NULL  
);

CREATE TABLE results (
        match_id integer REFERENCES matches(match_id) NOT NULL,
        winner integer REFERENCES players(player_id) NOT NULL,
        loser integer REFERENCES players(player_id) NOT NULL
);

INSERT INTO players (player_id, name) VALUES
        (default, 'Moe'), (default, 'Larry'),
        (default, 'Curly'), (default, 'Shemp'),
        (default, 'Curly Joe'), (default, 'Joe Curly');

INSERT INTO matches (match_id, match_date, player1, player2) VALUES
        (default, '6/1/2015', 1, 2),
        (default, '6/2/2015', 3, 2),
        (default, '6/4/2015', 1, 4);

INSERT INTO results (match_id, winner, loser) VALUES
        (1, 1, 2),
        (2, 3, 2),
        (3, 1, 4);

CREATE VIEW num_of_matches AS
  SELECT players.name, count(matches.match_id) AS total_matches
      FROM players
      LEFT JOIN matches
      ON players.player_id = matches.player1 OR players.player_id = matches.player2
      GROUP BY players.name
      ORDER BY total_matches DESC;


CREATE VIEW num_of_wins AS
  SELECT players.name, count(results.winner) AS total_wins
      FROM players
      LEFT JOIN results
      ON players.player_id = results.winner
      GROUP BY players.name
      ORDER BY total_wins DESC;



CREATE VIEW standings AS 
  SELECT players.name, players.player_id,
  (SELECT count(*) FROM results WHERE results.winner = players.player_id) as final_wins,
  (SELECT count(*) FROM matches WHERE matches.player1 = players.player_id
   OR matches.player2 = players.player_id) as final_matches
  FROM players, results, matches
  GROUP BY players.player_id
  ORDER BY final_wins DESC;






