import json
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def stacked_bar_graph(data):
    """Plot stacked bar graph of transportation types."""

    city_data = data['cities']
    t_types = data['transportation_types']
    city_names = [city_data[city_id]['name'] for city_id in city_data]
    colors = []
    for _ in range(len(t_types)):
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
    plt.show()

def bar_graph(data):
    """Plot bar graph of population data."""

    city_data = data['cities']
    city_names = [city_data[city_id]['name'] for city_id in city_data]
    y = []
    for city_id in city_data:
            city = city_data[city_id]
            population = city['population']
            y.append(population)
    
    plt.bar(city_names, y, color='r')

    plt.xlabel("Cities")
    plt.ylabel("Estimated Population")
    plt.title("Population For Cities")
    plt.show()


def scatter_plot(data):
    """Plot data points of population/transportation with air quality."""

    city_data = data['cities']
    city_names = []
    x = []
    y = []
    for city_id in city_data:
        city = city_data[city_id]
        air_quality = city['air_quality']
        if isinstance(air_quality, float):
            routes = sum([city['transportation'][route] for route in city['transportation']])
            x.append(routes)
            y.append(air_quality)
            city_names.append(city['name'])
    plt.xlabel("Transportation Routes")
    plt.ylabel("Average PM2.5 Air Quality")
    for i, txt in enumerate(city_names):
        plt.annotate(txt, (x[i], y[i]))
    plt.title("Transportation Routes and Air Quality")
    plt.scatter(x, y)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), color="r", linestyle=':', linewidth=1)
    plt.show()


def population_scatter_plot(data):
    """Plot data points of population/transportation with air quality."""

    city_data = data['cities']
    city_names = []
    x = []
    y = []
    for city_id in city_data:
        city = city_data[city_id]
        air_quality = city['air_quality']
        if isinstance(air_quality, float):
            routes = sum([city['transportation'][route] for route in city['transportation']])
            x.append(routes/city['population'])
            y.append(air_quality)
            city_names.append(city['name'])
    plt.xlabel("Transportation Routes per Capita")
    plt.ylabel("Average PM2.5 Air Quality")
    for i, txt in enumerate(city_names):
        plt.annotate(txt, (x[i], y[i]))
    plt.title("Transportation Routes per Capita and Air Quality")
    plt.scatter(x, y)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), color="r", linestyle=':', linewidth=1)
    plt.show()



def main():
    with open("processed.json", "r") as infile:
        processed_data = json.load(infile)
        stacked_bar_graph(processed_data)
        bar_graph(processed_data)
        scatter_plot(processed_data)
        population_scatter_plot(processed_data)


if __name__ == "__main__":
    main()