import json

def main():

    with open("processed.json", "r") as infile:
        processed_data = json.load(infile)

if __name__ == "__main__":
    main()