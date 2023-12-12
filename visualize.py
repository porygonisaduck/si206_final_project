import json
import matplotlib.pyplot as plt

def graph(data):
    pass


def main():

    with open("processed.json", "r") as infile:
        processed_data = json.load(infile)
        # for city_data in processed_data:
        graph(processed_data)
if __name__ == "__main__":
    main()