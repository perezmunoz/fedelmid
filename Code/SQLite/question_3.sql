# Who are the top 10% best paid players in the 2011-2012 season?
# Which teams did these players play for?
SELECT A.NAME, B.TEAM, B.SALARY 
	FROM PROFILEF A, SALARY B 
	WHERE A.PLAYERID = B.PLAYERID AND B.SEASON = 2011
		AND A.PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS WHERE ACTIVE = "TRUE")
	ORDER BY B.SALARY DESC
	LIMIT (SELECT CAST(COUNT(*)*0.1 AS INTEGER) FROM SALARY WHERE SEASON = 2011);
		
# Who are the bottom 10% worst paid players in the 2011-2012 season?
# Which teams did these players play for?
SELECT A.NAME, B.TEAM, B.SALARY 
	FROM PROFILEF A, SALARY B 
	WHERE A.PLAYERID = B.PLAYERID AND B.SEASON = 2011
		AND A.PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS WHERE ACTIVE = "TRUE")
	ORDER BY B.SALARY ASC
	LIMIT (SELECT CAST(COUNT(*)*0.1 AS INTEGER) FROM SALARY WHERE SEASON = 2011);

# Who are the middle 50% by pay?
# Which teams did they play for?		
SELECT A.NAME, B.TEAM
	FROM PROFILEF A, SALARY B 
	WHERE A.PLAYERID = B.PLAYERID AND B.SEASON = 2011
		AND A.PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS WHERE ACTIVE = "TRUE")
	ORDER BY B.SALARY ASC
	LIMIT  (SELECT CAST(COUNT(*)*0.5 AS INTEGER) FROM SALARY WHERE SEASON = 2011)
	OFFSET (SELECT CAST(COUNT(*)*0.25 AS INTEGER) FROM SALARY WHERE SEASON = 2011);
		
# Over all seasons of the active players in the 2011-2012 season,
# how much money was paid to all users by season? How many players were active in each season?
# What is the average per player by season? 

SELECT B.SEASON, SUM(B.SALARY), COUNT(*), AVG(B.SALARY)
FROM PROFILEF A, SALARY B 
WHERE A.PLAYERID = B.PLAYERID
AND A.PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS
		   WHERE ACTIVE = "TRUE")
GROUP BY SEASON;
 
 5.	What other data from the basketball-reference.com can you use to explain salary? You may wish to scrape more data from the website. What is your recommendation to team owners? How can you justify high prices for players?
