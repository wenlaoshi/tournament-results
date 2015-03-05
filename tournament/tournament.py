#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Connect to tournament database.
    db = connect()
    c = db.cursor()
    
    # Delete match data from scores table.
    c.execute("DELETE FROM score_data;")
    
    # Commit changes and close.
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # Connect to tournament database.
    db = connect()
    c = db.cursor()
    
    # Delete dependent table data in scores table.
    c.execute("DELETE FROM score_data;")
    
    # Delete player data
    c.execute("DELETE FROM players;")

    # Commit changes and close.
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # Connect to tournament database.
    db = connect()
    c = db.cursor()
    
    # Get number of registered players from players table.
    c.execute("SELECT COUNT(*) FROM players;")
    num = c.fetchone()[0]

    # Close database and return amount.
    db.close()   
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Connect to tournament database.
    db = connect()
    c = db.cursor()
    
    # Add cleansed new player name to players table. Id is automatically incremented.
    c.execute("INSERT INTO players (name) values (%s);", (bleach.clean(name),))

    # Commit changes and close.
    db.commit()
    db.close()


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
    # Connect to tournament database.
    db = connect()
    c = db.cursor()
    
    # Get all player scores from scores table with join from players table.. 
    # SUM returns NULL for players without an entry in scores, so use COALESCE function to get zero value.
    c.execute("""
    			SELECT players.id, players.name, COALESCE(SUM(score_data.points), 0) AS wins, COUNT(score_data.player_id) AS num 
    			FROM players LEFT JOIN score_data
    			ON players.id = score_data.player_id
    			GROUP BY players.id
    			ORDER BY wins DESC;
    			""")
    result = c.fetchall()
    db.close()
    
    # Assemble return values
    standings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3])) for row in result]
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Connect to tournament database.
    db = connect()
    c = db.cursor()
    
    # Insert match results into scores table.
    # Based on scoring system from BLAH winner receives 3 points, tie or bye receive 1, and losers none
    c.execute("INSERT INTO score_data (player_id, points) values (%s, %s);", (winner, 1))
    c.execute("INSERT INTO score_data (player_id, points) values (%s, %s);", (loser, 0))

    # Commit changes and close.
    db.commit()
    db.close()   

 
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
	# Get latest standings.
    standings = playerStandings()
    
    # Store in list of tuples two players per match.
    pairs = list()
    for n in range(0, len(standings), 2):
    	pairs.append([standings[n][0], standings[n][1], standings[n+1][0], standings[n+1][1]])
    	
    # Return paired list.
    return pairs
	

