import sqlite3
import json

def calculate_air_quality(city_id, cur, conn):
    """Compute weighted average of air quality for a city."""

    # retrieve observation counts and percents from database
    cur.execute("SELECT observation_count, observation_percent FROM air WHERE city_id = ?", (city_id,))
    observation_counts = cur.fetchall()

    # get total observation count
    observations = sum([observation[0] for observation in observation_counts])
    
    if observations > 0:

    # get a total sum of all observations
        sum_air_quality = sum([observation[0]*observation[1] for observation in observation_counts])

        # compute average air quality and return
        average_air_quality = sum_air_quality/observations
        return average_air_quality
    else:
        return 'N/A'

def calculate_transportation(city_id, cur, conn):
    """Sum up transportation routes for a city."""

    # retrieve transportation data from database
    cur.execute("SELECT transportation_type, COUNT(*) "
                "FROM transportation as T, typeOfTrans as S "
                "WHERE city_id = ? AND T.transportation_id = S.transportation_id "
                "GROUP BY S.transportation_type",
                (city_id,))
    t_data = cur.fetchall()

    # dictionary of transportation type to count
    t_dict = {}
    for data in t_data:
        t_dict[data[0]] = int(data[1])
    return t_dict

def get_population(city_id, cur, conn):
    """Get population count for a city."""

    # retrieve population from database
    cur.execute("SELECT population FROM cities WHERE city_id = ?", (city_id,))
    population = cur.fetchone()[0]
    return population

def main():

    conn = sqlite3.connect("final_database.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM cities")
    cities = cur.fetchall()

    # nested dictionary of city scores
    city_dict = {}

    # calculate and store scores for each city
    for city in cities:
        city_id = city[0]
        city_name = city[1]

        city_dict[city_id] = {}
        current = city_dict[city_id]
        current['name'] = city_name
        current['air_quality'] = calculate_air_quality(city_id, cur, conn)
        current['transportation'] = calculate_transportation(city_id, cur, conn)
        current['population'] = get_population(city_id, cur, conn)

    with open("processed.json", "w") as outfile:
        json.dump(city_dict, outfile)

if __name__ == "__main__":
    main()