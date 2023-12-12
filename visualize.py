import json
import matplotlib.pyplot as plt
import numpy as np

def graph(data):
    city_data = data['cities']
    t_types = data['transportation_types']
    city_names = [city_data[city_id]['name'] for city_id in city_data]
    y = []
    for type in t_types:
        current_y = []
        for city_id in city_data:
            city = city_data[city_id]
            t_data = city['transportation']
            if type in t_data:
                current_y.append(t_data[type])
            else:
                current_y.append(0)
        y.append(np.array(current_y))
    
    if len(y) > 0:
        plt.bar(city_names, y[0], color='r')
        prev = y[0]
        if len(y) > 1:
            for current in y[1:]:
                plt.bar(city_names, current, bottom=prev, color='b')
                prev += current

    plt.show()

def main():
    with open("processed.json", "r") as infile:
        processed_data = json.load(infile)
        # for city_data in processed_data:
        graph(processed_data)

if __name__ == "__main__":
    main()