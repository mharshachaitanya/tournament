-- Table definitions for the tournament project.
-- connect to tournament
\c tournament;
-- Create Players Table
CREATE TABLE PLAYERS(
	PLAYER_ID 		SERIAL 	PRIMARY KEY     NOT NULL,
	NAME     		TEXT    NOT NULL   
);
-- Create Matches 
CREATE TABLE MATCH_RESULTS(	
	MATCH_ID	SERIAL 	PRIMARY KEY     NOT NULL,
	WINNER_ID	INTEGER REFERENCES PLAYERS(PLAYER_ID),
	LOSER_ID	INTEGER REFERENCES PLAYERS(PLAYER_ID)
);
-- create view for Player Standings
CREATE VIEW playerstandings AS SELECT player_id as id,  name, (SELECT COUNT(*) FROM match_results WHERE players.player_id = match_results.winner_id ) As wins, (SELECT COUNT(*) FROM match_results WHERE (players.player_id = match_results.winner_id or players.player_id = match_results.loser_id))As matches from players order by wins DESC;