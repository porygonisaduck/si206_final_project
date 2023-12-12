import json
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def bar_graph(data):

    plt.subplot(211)
    
    city_data = data['cities']
    t_types = data['transportation_types']
    city_names = [city_data[city_id]['name'] for city_id in city_data]
    colors = []
    for i in range(len(t_types)):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
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
        plt.bar(city_names, y[0], color=colors.pop())
        prev = y[0]
        if len(y) > 1:
            for current in y[1:]:
                plt.bar(city_names, current, bottom=prev, color=colors.pop())
                prev += current

    plt.xlabel("Cities")
    plt.ylabel("Transportation Routes")
    plt.legend(t_types)
    plt.title("Transportation Route Totals For Cities")


def scatter_plot(data):

    plt.subplot(212)

    city_data = data['cities']
    city_names = [city_data[city_id]['name'] for city_id in city_data]
    colors = []
    for i in range(len(city_names)):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    x = []
    y = []
    for city_id in city_data:
        city = city_data[city_id]
        air_quality = city['air_quality']
        if isinstance(air_quality, float):
            x.append(city['population']/len(city['transportation']))
            y.append(air_quality)
    plt.xlabel("Average PM2.5 Air Quality")
    plt.ylabel("City Population per Transportation Routes")
    plt.legend(city_names)
    plt.title("Per Capita Transportation and Air Quality")
    plt.scatter(x, y)


def main():
    with open("processed.json", "r") as infile:
        processed_data = json.load(infile)
        # for city_data in processed_data:
        bar_graph(processed_data)
        scatter_plot(processed_data)
        plt.show()


if __name__ == "__main__":
    main()