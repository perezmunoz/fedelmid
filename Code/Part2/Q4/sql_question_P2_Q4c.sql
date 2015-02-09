select "Atlanta Hawks" as team,
 avg(case when season = 2002 then age end) as "2002",
 avg(case when season = 2003 then age end) as "2003",
 avg(case when season = 2004 then age end) as "2004",
 avg(case when season = 2005 then age end) as "2005",
 avg(case when season = 2006 then age end) as "2006",
 avg(case when season = 2007 then age end) as "2007",
 avg(case when season = 2008 then age end) as "2008",
 avg(case when season = 2009 then age end) as "2009",
 avg(case when season = 2010 then age end) as "2010",
 avg(case when season = 2011 then age end) as "2011" 
from player_total where team <> "" 
 	                  and season between 2002 and 2011 
 	                  and team = "ATL" group by team 
union all 
select "Boston Celtics" as team, 
 avg(case when season = 2002 then age end) as "2002", 
 avg(case when season = 2003 then age end) as "2003", 
 avg(case when season = 2004 then age end) as "2004",
 avg(case when season = 2005 then age end) as "2005",
 avg(case when season = 2006 then age end) as "2006",
 avg(case when season = 2007 then age end) as "2007",
 avg(case when season = 2008 then age end) as "2008",
 avg(case when season = 2009 then age end) as "2009",
 avg(case when season = 2010 then age end) as "2010",
 avg(case when season = 2011 then age end) as "2011" 
from player_total where team <> "" 
                    and season between 2002 and 2011 
                    and team = "BOS" group by team 
union all 
select "Miami Heat" as team, 
 avg(case when season = 2002 then age end) as "2002", 
 avg(case when season = 2003 then age end) as "2003", 
 avg(case when season = 2004 then age end) as "2004",
 avg(case when season = 2005 then age end) as "2005",
 avg(case when season = 2006 then age end) as "2006",
 avg(case when season = 2007 then age end) as "2007",
 avg(case when season = 2008 then age end) as "2008",
 avg(case when season = 2009 then age end) as "2009",
 avg(case when season = 2010 then age end) as "2010",
 avg(case when season = 2011 then age end) as "2011" 
from player_total where team <> "" 
                    and season between 2002 and 2011 
                    and team = "MIA" group by team

 	.......... 
 union all	
 select "Washington Wizards" as team, 
  avg(case when season = 2002 then age end) as "2002", 
  avg(case when season = 2003 then age end) as "2003", 
  avg(case when season = 2004 then age end) as "2004",
  avg(case when season = 2005 then age end) as "2005",
  avg(case when season = 2006 then age end) as "2006",
  avg(case when season = 2007 then age end) as "2007",
  avg(case when season = 2008 then age end) as "2008",
  avg(case when season = 2009 then age end) as "2009",
  avg(case when season = 2010 then age end) as "2010",
  avg(case when season = 2011 then age end) as "2011" 
 from player_total where team <> "" 
                     and season between 2002 and 2011 
                     and team = "WAS" group by team;
