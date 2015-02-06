# What is the average salary of each team by season of each team starting in 2002 and finishing 2012 season?
SELECT TEAM, SEASON, AVG(SALARY)
FROM SALARY WHERE SEASON BETWEEN 2002 AND 2011
GROUP BY TEAM, SEASON;

# What is the variance of the salaries?


# What is the average age of the players by season?
SELECT B.SEASON, B.TEAM, AVG(DATE('now')-A.DOB)
FROM PROFILEF A, PLAYER_TOTAL B
WHERE A.PLAYERID = B.PLAYERID
  AND A.PLAYERID IN (SELECT PLAYERID FROM ACTIVEPLAYERS WHERE ACTIVE = "TRUE")
  AND B.TEAM <> ""
  AND B.SEASON BETWEEN 2002 AND 2011
GROUP BY SEASON, TEAM;

# Average and variance of experience by season of each team?


# Can you provide the above in a "cross tabulation" format?
# That is, teams are on each row, each column is a year, and the values are the metrics above?
