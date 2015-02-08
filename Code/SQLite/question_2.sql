# How many active players there are during the 2011-2012 season?
SELECT COUNT(*) AS "ACTIVE PLAYERS"
FROM (SELECT DISTINCT A.PLAYERID
	FROM ACTIVEPLAYERS A, PLAYER_TOTAL B
	WHERE A.PLAYERID = B.PLAYERID
	  AND ACTIVE = "TRUE"
	  AND B.SEASON = 2011
          AND B.TEAM <> "");

# How many play in each position?
SELECT POSITION, COUNT(*) AS TOTALS
FROM (SELECT DISTINCT A.PLAYERID, B.POSITION 
        FROM ACTIVEPLAYERS A, PLAYER_TOTAL B
        WHERE A.ACTIVE = "TRUE"
          AND A.PLAYERID = B.PLAYERID
          AND B.SEASON = 2011
          AND B.TEAM <> "")
GROUP BY POSITION;

# What is the average age, average weight, average experience, average salary in the season, average career salary?

#average salary in the season, average career salary
WITH s1 AS
	(SELECT SUM(salary) as c_sal, playerid
	 FROM salary
 	 WHERE season < 2012 AND playerid IN (SELECT playerid FROM activeplayers WHERE active = "TRUE")
 	 GROUP BY playerid)
SELECT avg(a.salary) as AVG_SALARY
      ,avg(b.c_sal)  as AVG_CAREER_SALARY
	FROM salary a, s1 b
	WHERE a.playerid IN (SELECT playerid FROM activeplayers WHERE active = "TRUE")
		AND a.playerid = b.playerid
		AND b.season = 2011;

#average age, weight		
SELECT avg(b.age) as AVG_AGE
      ,avg(a.weight) as AVG_WEIGHT
	FROM profilef a, player_total b
	WHERE a.playerid IN (SELECT playerid FROM activeplayers WHERE active = "TRUE")
		AND a.playerid = b.playerid
		AND b.season = 2011;

#average experience
select avg(exp) 
from (select distinct a.playerid, a.experience as exp 
      from teamsroster a, activeplayers b 
      where a.playerid = substr(b.playerid,2) 
        and b.active = "TRUE" 
        and a.season = 2011);

