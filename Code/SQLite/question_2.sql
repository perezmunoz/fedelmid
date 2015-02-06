# How many active players there are during the 2011-2012 season?
SELECT COUNT(*)
FROM (SELECT DISTINCT A.PLAYERID
	FROM PROFILEF A, PLAYER_TOTAL B
	WHERE PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS WHERE ACTIVE = "TRUE")
	  AND A.PLAYERID = B.PLAYERID
	  AND B.SEASON = 2011
          AND B.TEAM <> "");

# How many play in each position?
	 SELECT POSITION, COUNT(*)
	 FROM (SELECT DISTINCT A.PLAYERID, B.POSITION 
               FROM PROFILEF A, PLAYER_TOTAL B
               WHERE A.PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS WHERE ACTIVE = "TRUE")
                 AND A.PLAYERID = B.PLAYERID
                 AND B.SEASON = 2011
		 AND B.TEAM <> "")
	 GROUP BY X.POSITION;

# What is the average age, average weight, average experience, average salary in the season, average career salary?
WITH s1 AS
	(SELECT SUM(salary) as c_sal, playerid
	 FROM salary
 	 WHERE season < 2014 AND playerid IN (SELECT playerid FROM activeplayers WHERE active = "TRUE")
 	 GROUP BY playerid)
SELECT avg(date('now')-a.dob)
      ,avg(a.weight)
      ,avg(a.experience)
      ,avg(b.salary)
      ,avg(c.c_sal)
	FROM profilef a, salary b, s1 c
	WHERE a.playerid IN (SELECT playerid FROM activeplayers WHERE active = "TRUE")
		AND a.playerid = b.playerid
		AND a.playerid = c.playerid
		AND b.season = 2011;
