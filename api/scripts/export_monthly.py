import sqlite3
import pandas


conn = sqlite3.connect("db.sqlite3")

query = """
    SELECT
        driver.first_name || ' ' || driver.last_name AS driver_name,
        STRFTIME('%Y-%m', rideevent_dropoff.created) AS month,
        COUNT(*) AS trips_over_1_hour
    FROM api_ride ride
    JOIN api_rideuser driver ON ride.driver_id = driver.id
    JOIN api_rideevent rideevent_pickup 
        ON ride.id = rideevent_pickup.ride_id 
        AND rideevent_pickup.description LIKE 'Driver is on the way%'
    JOIN api_rideevent rideevent_dropoff 
        ON ride.id = rideevent_dropoff.ride_id 
        AND rideevent_dropoff.description LIKE 'Arrived at destination%'
    WHERE 
        JULIANDAY(rideevent_dropoff.created) - JULIANDAY(rideevent_pickup.created) > (1.0 / 24.0) -- 1 hour
    GROUP BY driver_name, STRFTIME('%Y-%m', rideevent_dropoff.created)
"""

dataframe = pandas.read_sql_query(query, conn)
dataframe.to_excel("driver_trips_over_1_hour.xlsx", index=False)

conn.close()
print("Export completed: driver_trips_over_1_hour.xlsx")