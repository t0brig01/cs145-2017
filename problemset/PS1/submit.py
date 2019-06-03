import sqlite3
from prettytable import from_db_cursor

# copy and paste your SQL queries into each of the below variables
# note: do NOT rename variables

Q1 = '''
SELECT AVG(arr_delay) 
FROM flight_delays 
WHERE month=7 AND year=2017
'''

Q2 = '''
SELECT MAX(arr_delay) 
FROM flight_delays 
WHERE month=7 AND year=2017
'''

Q3 = '''
SELECT carrier,fl_num,origin_city_name,dest_city_name,fl_date 
FROM flight_delays
WHERE arr_delay=1895
'''

Q4 = '''
SELECT weekdays.weekday_name AS weekday_name, AVG(arr_delay) AS average_delay 
FROM flight_delays 
INNER JOIN weekdays ON flight_delays.day_of_week = weekdays.weekday_id
GROUP BY day_of_week 
ORDER BY day_of_week 
'''

Q5 = '''
SELECT airlines.airline_name, AVG(f.arr_delay)
FROM flight_delays f
JOIN airlines ON f.airline_id = airlines.airline_id
WHERE f.airline_id IN(
    SELECT DISTINCT airline_id
    FROM flight_delays
    WHERE origin = "SFO"
    GROUP BY airline_id
    HAVING COUNT(airline_id) >= 1
)
GROUP BY f.airline_id
ORDER BY avg(f.arr_delay) DESC
'''

Q6 = '''
SELECT CAST(x.count as float)/CAST(y.count as float)
FROM(
    SELECT COUNT(*) AS count
    FROM(
        SELECT COUNT(airline_id)
        FROM flight_delays
        GROUP BY airline_id
        HAVING avg(arr_delay) >= 10
    )
)x,
(
        SELECT COUNT(*) AS count
    FROM(
        SELECT COUNT(airline_id)
        FROM flight_delays
        GROUP BY airline_id
    )
)y
'''

Q7 = '''
SELECT 1.0/(n-1) * SUM((dep_delay - x_bar) * (arr_delay - y_bar))
FROM flight_delays,(
    SELECT COUNT(*) as n,
        avg(dep_delay) as x_bar, 
        avg(arr_delay) as y_bar
    FROM flight_delays
)
'''

Q8 = '''
SELECT DISTINCT a.airline_name, MAX(l.last_avg - f.first_avg) as delay_increase
FROM 
   (
       SELECT f.airline_id, AVG(arr_delay) as first_avg
       FROM flight_delays f
       WHERE day_of_month < 24
       group by f.airline_id
   ) f
   JOIN
   (
       SELECT f.airline_id, AVG(arr_delay) as last_avg
       FROM flight_delays f
       WHERE day_of_month >= 24
       group by f.airline_id

   ) l
   ON f.airline_id = l.airline_id
JOIN airlines a ON l.airline_id = a.airline_id
'''

Q9 = '''
SELECT DISTINCT a.airline_name
FROM flight_delays f, airlines a
JOIN airlines ON f.airline_id = a.airline_id
WHERE origin = "SFO" AND f.airline_id IN(
    SELECT airline_id
    FROM flight_delays
    WHERE dest = "PDX"
) AND dest = "EUG"
'''

Q10 = '''
SELECT origin,dest,avg(arr_delay)
FROM flight_delays
WHERE ((origin = "MDW" or origin = "ORD") and (dest = "SFO" or dest = "SJC" or dest = "OAK") and (crs_dep_time > 1400))
group by origin,dest
order by avg(arr_delay) desc
'''

#################################
# do NOT modify below this line #
#################################

# open a database connection to our local flights database
def connect_database(database_path):
    global conn
    conn = sqlite3.connect(database_path)

def get_all_query_results(debug_print = True):
    all_results = []
    for q, idx in zip([Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10], range(1, 11)):
        result_strings = ("The result for Q%d was:\n%s\n\n" % (idx, from_db_cursor(conn.execute(q)))).splitlines()
        all_results.append(result_strings)
        if debug_print:
            for string in result_strings:
                print string
    return all_results

if __name__ == "__main__":
    connect_database('flights.db')
    query_results = get_all_query_results()