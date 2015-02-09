SELECT COUNT(*) AS “Active_Players”
FROM (SELECT DISTINCT A.PLAYERID
	FROM ACTIVEPLAYERS A, PLAYER_TOTAL B
	WHERE A.PLAYERID = B.PLAYERID
	  AND ACTIVE = "TRUE"
	  AND B.SEASON = 2011
          AND B.TEAM <> "");

SELECT POSITION, COUNT(*)
FROM (SELECT DISTINCT A.PLAYERID, B.POSITION 
        FROM ACTIVEPLAYERS A, PLAYER_TOTAL B
        WHERE A.ACTIVE = "TRUE"
          AND A.PLAYERID = B.PLAYERID
          AND B.SEASON = 2011
          AND B.TEAM <> "")
GROUP BY POSITION;

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
		AND a.season = 2011;

SELECT avg(b.age) as AVG_AGE
      ,avg(a.weight) as AVG_WEIGHT
	FROM profilef a, player_total b
	WHERE a.playerid IN (SELECT playerid FROM activeplayers WHERE active = "TRUE")
		AND a.playerid = b.playerid
		AND b.season = 2011;

select avg(exp) as AVG_EXPERIENCE
from (select distinct a.playerid, a.experience as exp 
      from teamsroster a, activeplayers b 
      where a.playerid = substr(b.playerid,2) 
        and b.active = "TRUE" 
        and a.season = 2011);