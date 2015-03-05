-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create tournament database.
CREATE DATABASE tournament;

-- Create players table to store individual player information
-- containing a primary key a player id and player name.
CREATE TABLE players (
	id serial primary key,
	name text
);

-- Create score table to store the results of each match
-- containing foreign keys referencing players id.
-- Two rows, one for each player, win is 0 for a loss and 1 for a win.
CREATE TABLE score_data (
	id serial primary key,
	player_id integer references players (id),
	points integer
);

