SELECT SEASON, AVG(AGE)
	FROM PLAYER_TOTAL
	WHERE TEAM <> "" AND SEASON BETWEEN 2002 AND 2011
	GROUP BY SEASON;

SELECT season, team_id, AVG(experience), SUM((experience-(SELECT AVG(experience)
															FROM teamsroster
															WHERE season between 2002 AND 2011))*(experience-(SELECT avg(experience)
																												FROM teamsroster
																												WHERE season between 2002 AND 2011)))/(count(experience)-1)
	FROM teamsroster
	WHERE season between 2002 AND 2011
	GROUP BY season, team_id;