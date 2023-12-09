import sqlite3

def calculate_air_score(city_id):
    pass

def calculate_transportation_score(city_id):
    pass

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
        current['air_score'] = calculate_air_score(city_id)
        current['transportation_score'] = calculate_transportation_score(city_id)

if __name__ == "__main__":
    main()