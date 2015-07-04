#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        cdb = psycopg2.connect("dbname={}".format(database_name))
        c = cdb.cursor()
        return cdb, c
    except:
        print("Cannnot connect to database")


def deleteMatches():
    """Removes all results records such as wins, lossses and match id's from the database"""
    cdb, c = connect()
    cmd = ("DELETE FROM results;")
    c.execute(cmd)
    cdb.commit()
    cdb.close()


def deletePlayers():
    """Removes all the player records from the database."""
    cdb, c = connect()
    cmd = ("DELETE FROM players;")
    c.execute(cmd)
    cdb.commit()
    cdb.close()


def countPlayers():
    """Returns the number of players ready to play a match."""
    cdb, c = connect()
    cmd = ("SELECT count(players.player_id) AS player_count FROM players;")
    c.execute(cmd)
    player_count = c.fetchall()[0][0]
    return player_count
    cdb.close()
 

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    Args:
      name: the player's full name (need not be unique).
    """
    cdb, c = connect()
    cmd = ("INSERT INTO players(player_id, name) VALUES (default, %s);") 
    c.execute(cmd, (name,))
    cdb.commit()
    cdb.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cdb, c = connect()
    cmd = ("SELECT * FROM standings;")
    c.execute(cmd)
    matches = c.fetchall()
    return matches
    cdb.close()
 

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cdb, c = connect()
    cmd = ("INSERT INTO results(match_id, winner, loser) VALUES (default, %s, %s);") 
    c.execute(cmd, (winner,loser,))
    cdb.commit()
    cdb.close()
 
 
def swissPairings():
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
    cdb, c = connect()
    cmd = ("SELECT player_id, name FROM standings WHERE total_wins = total_wins")
    c.execute(cmd)
    win_pair_list = c.fetchall()
    pairing1 = win_pair_list[0] + win_pair_list[1]
    pairing2 = win_pair_list[2] + win_pair_list[3]
    pair.append(pairing1)
    pair.append(pairing2)
    return pair
    cdb.close()

