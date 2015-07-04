#!/usr/bin/env python
#
"""
Unit tests that are run to check the integrity of tournament.py and the
Swiss tournament pairings

"""
from tournament import *


def test_delete_matches():

    """ runs the delete_matches function in tournament.py to make sure
    the results table is cleared out
    """

    delete_matches()
    print "1. Old matches can be deleted."


def test_delete():

    """runs the delete_matches & delete_players function tournament.py
    to make sure that both the results & players table are empty
    """

    delete_matches()
    delete_players()
    print "2. Player records can be deleted."


def test_count():

    """runs delete_matches & delete players functions to clear out
    results and players table.
    Then stores player_count from the count_players function in a
    variable and checks to make sure the players table is empty.
    """

    delete_matches()
    delete_players()
    c = count_players()
    if c == '0':
        raise TypeError(
            "count_players() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print "3. After deleting, count_players() returns zero."


def test_register():

    """runs delete_matches, delete players to clear out
    players and results table.
    Then runs register_player function with one player name as an argument
    After registering the player it runs count_players to make sure that
    there are players in the players table.

    """
    delete_matches()
    delete_players()
    register_player("Chandra Nalaar")
    c = count_players()
    if c != 1:
        raise ValueError(
            "After one player registers, count_players() should be 1.")
    print "4. After registering a player, count_players() returns 1."


def test_register_count_delete():

    """runs delete_matches & delete_players to clear out
    players and results table.
    Will run register_player function on four player names.
    Runs count_players to make sure there are exactly 4 players.
    Runs delete_players to clear out players table.
    Then runs count_players again to make sure there are 0 players.
    """
    delete_matches()
    delete_players()
    register_player("Markov Chaney")
    register_player("Joe Malik")
    register_player("Mao Tsu-hsi")
    register_player("Atlanta Hope")
    c = count_players()
    if c != 4:
        raise ValueError(
            "After registering four players, count_players should be 4.")
    delete_players()
    c = count_players()
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print "5. Players can be registered and deleted."


def test_standings_before_matches():

    """
    runs delete_matches & delete_players to clear out
    players and results table.

    Will run register_player function on two player names.
    standings() is stored in a variable and checked to make sure
    that the players are listed in the standings table and that
    there are exactly four columns with no data.
    """

    delete_matches()
    delete_players()
    register_player("Melpomene Murray")
    register_player("Randy Schwartz")
    standings = player_standings()
    if len(standings) < 2:
        raise ValueError("Players should appear in player_standings even "
                         "before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings")
    if len(standings[0]) != 4:
        raise ValueError("Each player_standings row should have four columns")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in, "
                         "standings even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches"


def test_report_matches():

    """
    runs delete_matches & delete_players to clear out
    players and results table.

    Will run register_player function on four player names.
    standings() is stored in a variable.

    Runs report_match function on two sets of players id's
    to record a winner and loser.

    standings is checked to make sure that each player has one match
    recorded, and each winner and loser has been properly recorded
    """

    delete_matches()
    delete_players()
    register_player("Bruno Walton")
    register_player("Boots O'Neal")
    register_player("Cathy Burton")
    register_player("Diane Grant")
    standings = player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)
    standings = player_standings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded")
    print "7. After a match, players have updated standings."


def test_pairings():

    """
    runs delete_matches & delete_players to clear out
    players and results table.

    Will run register_player function on four player names.
    standings() is stored in a variable.

    Runs report_match function on two sets of players id's
    to record a winner and loser.

    swiss_pairings() is stored in a variable and checked to make sure that
    a tuple containing a pairing of two players is returned.
    """

    delete_matches()
    delete_players()
    register_player("Twilight Sparkle")
    register_player("Fluttershy")
    register_player("Applejack")
    register_player("Pinkie Pie")
    standings = player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)

    pairings = swiss_pairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swiss_pairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    test_delete_matches()
    test_delete()
    test_count()
    test_register()
    test_register_count_delete()
    test_standings_before_matches()
    test_report_matches()
    test_pairings()
    print "Success!  All tests pass!"
