#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
"""
Functions that tournament_test.py will run unit tests on.
This program represents the first two rounds of a Swiss Tournament.

"""


import psycopg2


def connect(database_name="tournament"):

    """Creates database db_connection and cursor object """

    try:
        db_connect = psycopg2.connect("dbname={}".format(database_name))
        cursor = db_connect.cursor()
        return db_connect, cursor
    except psycopg2.Error:
        print "Cannot db_connect to database"


def delete_matches():

    """Removes all results records such as wins, lossses and match
    id's from the database
    """
    db_connect, cursor = connect()
    query = ("TRUNCATE results CASCADE;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def delete_players():

    """Removes all the player records from the database."""
    db_connect, cursor = connect()
    query = ("TRUNCATE players CASCADE;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def count_players():

    """Returns the number of players ready to play a match."""
    db_connect, cursor = connect()
    query = ("SELECT count(players.player_id) AS player_count FROM players;")
    cursor.execute(query)
    player_count = cursor.fetchall()[0][0]
    db_connect.close()
    return player_count


def register_player(name):

    """Adds a player to the tournament database.
    Args:
      name: the player's full name (need not be unique).
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
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
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
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
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
