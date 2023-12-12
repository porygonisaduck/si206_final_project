import sqlite3
import json

def create_city_dict(cur, conn):
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
    
    return city_dict

def create_transportation_types_list(cur, conn):
    cur.execute("SELECT DISTINCT transportation_type FROM typeOfTrans")
    types = cur.fetchall()
    return [type[0] for type in types]

def calculate_air_quality(city_id, cur, conn):
    """Compute average air quality for a city."""

    # retrieve PM2.5 observations
    cur.execute("SELECT PM25 FROM air WHERE city_id = ?", (city_id,))
    observations = cur.fetchall()

    if len(observations) > 0:
    # compute avurage PM2.5
        return sum([pm25[0] for pm25 in observations])/len(observations)
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

    # create database connection and get cursor
    conn = sqlite3.connect("final_database.db")
    cur = conn.cursor()

    # process data into a dictionary
    processed_data = {'cities': create_city_dict(cur, conn), 
                      'transportation_types': create_transportation_types_list(cur, conn)}

    # output dictionary into json file
    with open("processed.json", "w") as outfile:
        json.dump(processed_data, outfile)

if __name__ == "__main__":
    main()