#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	try:
		return psycopg2.connect("dbname=tournament")
	except:
		print "unable to connect to the database."

def deleteMatches():
	"""Remove all the match records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("DELETE  from MATCH_RESULTS")
	db.commit() 
	db.close()
	
def deletePlayers():
	"""Remove all the player records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("DELETE  from PLAYERS")
	db.commit() 
	db.close()

def countPlayers():
	"""Returns the number of players currently registered."""
	db = connect()
	c = db.cursor()
	c.execute("select count(*) from players")
	count = c.fetchone()[0]
	db.close()
	return count

def registerPlayer(name):
	"""Adds a player to the tournament database.
	The database assigns a unique serial id number for the player.
	(Thisshould be handled by your SQL database schema, not in your Python code.)
	Args:
		name: the player's full name (need not be unique).
	"""
	db = connect()
	c = db.cursor()
	c.execute("INSERT INTO PLAYERS(NAME) VALUES (%s)" ,(name,))	
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
	db = connect()
	c = db.cursor()
	c.execute("select id, name, wins, matches from playerstandings")
	standings = c.fetchall()
	db.commit() 
	db.close()
	return standings

def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.
	Args:
		winner:  the id number of the player who won
		loser:  the id number of the player who lost
	"""
	db = connect()
	c = db.cursor()
	c.execute("INSERT INTO MATCH_RESULTS(WINNER_ID, LOSER_ID) VALUES (%s, %s)" ,(winner,loser,))	
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
	standings = playerStandings()
	tmp_list = []
	swiss_pairings = []
	for rank, player in enumerate(standings):
		if rank % 2 == 0:
			tmp_list.append(player[0])
			tmp_list.append(player[1]) 
		else:
			tmp_list.append(player[0])
			tmp_list.append(player[1])
			swiss_pairings.append(tuple(tmp_list))
			tmp_list = []
	return swiss_pairings

