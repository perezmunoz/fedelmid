WITH sample AS (SELECT a.playerid, b.name, a.team, a.salary
					FROM salary a, profilef b
					WHERE a.playerid = b.playerid
						AND b.playerid IN (SELECT playerid
												FROM activeplayers
												WHERE active = "TRUE")
						AND a.season = 2011)
	SELECT name, team, salary
		FROM sample
		ORDER BY salary ASC LIMIT (SELECT CAST(COUNT(*)*0.1 AS INTEGER) FROM sample);