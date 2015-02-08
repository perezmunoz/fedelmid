# What is the average salary of each team by season of each team starting in 2002 and finishing 2012 season?
SELECT TEAM, SEASON, AVG(SALARY)
FROM SALARY WHERE SEASON BETWEEN 2002 AND 2011
GROUP BY TEAM, SEASON;

# What is the variance of the salaries?
SELECT SEASON, TEAM, SUM((SALARY-(SELECT AVG(SALARY) FROM SALARY WHERE SEASON BETWEEN 2002 AND 2011)) *
                         (SALARY-(SELECT AVG(SALARY) FROM SALARY WHERE SEASON BETWEEN 2002 AND 2011))) /
                         (COUNT(SALARY)-1)
FROM SALARY WHERE SEASON BETWEEN 2002 AND 2011
GROUP BY SEASON, TEAM;

# What is the average age of the players by season?
SELECT SEASON, AVG(AGE)
FROM PLAYER_TOTAL 
WHERE TEAM <> ""
  AND SEASON BETWEEN 2002 AND 2011
GROUP BY SEASON;

# Average and variance of experience by season of each team?
select season
       ,teamid
       ,avg(experience)
       ,sum((experience-(select avg(experience) from teamroster where season between 2002 and 2011))*
            (experience-(select avg(experience) from teamroster where season between 2002 and 2011)))/
            (count(experience)-1) 
from teamroster 
where season between 2002 and 2011 
group by season,teamid;

# Can you provide the above in a "cross tabulation" format?
select team,   
       avg(case when season = 2002 then salary end) as "2002"
      ,avg(case when season = 2003 then salary end) as "2003"
      ,avg(case when season = 2004 then salary end) as "2004"
      ,avg(case when season = 2005 then salary end) as "2005"
      ,avg(case when season = 2006 then salary end) as "2006"
      ,avg(case when season = 2007 then salary end) as "2007"
      ,avg(case when season = 2008 then salary end) as "2008"
      ,avg(case when season = 2009 then salary end) as "2009"
      ,avg(case when season = 2010 then salary end) as "2010"
      ,avg(case when season = 2011 then salary end) as "2011"
from salary where season between 2002 and 2011
group by team;


# That is, teams are on each row, each column is a year, and the values are the metrics above?
