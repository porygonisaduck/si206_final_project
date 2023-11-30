import json

def read_json(file):
    with open(file) as in_file:
        return json.load(in_file)


def main():
    networks = read_json('available_networks.json')
    
    locations = []
    for network in networks["networks"]:
        if network["network_location"] not in locations:
            locations.append(network["network_location"])

    locations.sort()
    print(*locations, sep="\n")

if __name__ == "__main__":
    main()