import sqlite3
import json

def calculate_air_score(city_id, cur, conn):
    # TODO: way to calculate air score
    score = 1
    return score

def calculate_transportation_score(city_id, cur, conn):
    cur.execute("SELECT population FROM cities WHERE city_id = ?", (city_id,))
    population = cur.fetchone()[0]
    # TODO: way to calculate transportation score
    score = 1
    return score/population

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
        current['air_score'] = calculate_air_score(city_id, cur, conn)
        current['transportation_score'] = calculate_transportation_score(city_id, cur, conn)

    with open("processed.json", "w") as outfile:
        json.dump(city_dict, outfile)

if __name__ == "__main__":
    main()