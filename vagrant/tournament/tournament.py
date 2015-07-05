#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
"""
Functions that tournament_test.py will run unit tests on.
This program represents the first two rounds of a Swiss Tournament.

"""


import psycopg2


def connect(database_name="tournament"):

    """Creates database connection and cursor object, throws exception if
    there is a connection error"""

    try:
        db_connect = psycopg2.connect("dbname={}".format(database_name))
        cursor = db_connect.cursor()
        return db_connect, cursor
    except psycopg2.Error:
        print "Cannot db_connect to database"


def delete_matches():

    """Removes all results records such as wins, lossses and match
    id's from the database.

    'query' stores the postgresql commands to be executed by the
    cursor object which wipes the table.

    db_connect() commits changes and closes the database.
    """

    db_connect, cursor = connect()
    query = ("DELETE FROM results;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def delete_players():

    """Removes all the player records from the database.

    'query' stores the posgresql commands to be executed by the
    cursor object which wipes the table.

    db_connect() commits changes and closes the database.
    """

    db_connect, cursor = connect()
    query = ("DELETE FROM players;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def count_players():

    """Returns the number of players ready to play a match.

    'query' stores the postgresql commands to be executed by the
    cursor object which will return a count of all the players
    in the players table.

    'player_count' stores the list of  players tuples
    returned by database.

    db_connect() closes the database.
    """

    db_connect, cursor = connect()
    query = ("SELECT count(players.player_id) AS player_count FROM players;")
    cursor.execute(query)
    player_count = cursor.fetchone()[0]
    db_connect.close()
    return player_count


def register_player(name):

    """Adds a player to the tournament database.
    Args:
      name: the player's full name (need not be unique).
      player_id is set by the database.

    'query' stores the postgresql commands to be executed by the
    cursor object which inserts a new player name and id into the
    table.

    query parameter 'name' is used to protect the database from
    sql based attacks.

    db_connect() commits changes and closes the database.
    """

    db_connect, cursor = connect()
    query = ("INSERT INTO players(player_id, name) VALUES (default, %s);")
    cursor.execute(query, (name,))
    db_connect.commit()
    db_connect.close()


def player_standings():

    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    'query' stores the postgresql commands to be executed by the
    cursor object which selects all the data from the
    standings view.

    'matches' collects the data as a list of tuples and returns it.

    db_connect() commits changes and closes the database.
    """

    db_connect, cursor = connect()
    query = ("SELECT * FROM standings;")
    cursor.execute(query)
    matches = cursor.fetchall()
    db_connect.close()
    return matches


def report_match(winner, loser):

    """Records the outcome of a single match between two players.
    Args:
      winner:  player_id of the player who won
      loser:  player_id of the player who lost

    'query' stores the postgresql commands to be executed by the
    cursor object which inserts a player name and id as winner
    and loser, into the results table.

    query parameters 'winner' and 'loser' are used to protect the database from
    sql based attacks.

    db_connect() commits changes and closes the database.
    """

    db_connect, cursor = connect()
    query = ("INSERT INTO results(match_id, winner, loser) \
              VALUES (default, %s, %s);")
    cursor.execute(query, (winner, loser,))
    db_connect.commit()
    db_connect.close()


def swiss_pairings():

    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's player_id
        name1: the first player's name
        id2: the second player's player_id
        name2: the second player's name

    'query' stores the postgresql commands to be executed by the
    cursor object which collects a list of players tuples where the
    total_wins column in the standings view is the same.

    'win_pair_list' stores the list of tuples returned by database.

    'pairing1' and 'pairing2' are assigned the concatenation of each
    player tuple pairing that includes the player_id and name.

    'pairing1' and 'pairing2' are then appended to the empty pair list to
    create a pair of tuples.

    The pair of tuples are then returned for use in the next round of the
    tournament.
    """

    pair = []
    db_connect, cursor = connect()
    query = ("SELECT player_id, name \
              FROM standings \
              WHERE total_wins = total_wins")
    cursor.execute(query)
    win_pair_list = cursor.fetchall()

    pairing1 = win_pair_list[0] + win_pair_list[1]
    pairing2 = win_pair_list[2] + win_pair_list[3]

    pair.append(pairing1)
    pair.append(pairing2)
    db_connect.close()

    return pair
