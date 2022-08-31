import json

with open("config.json") as f:
        json_data = json.load(f)
        if json_data["ip1"] is not None:
            print(json_data["ip1"])