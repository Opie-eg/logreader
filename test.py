import json

with open("config.json") as f:
    json_data = json.load(f)
    server_list = []
    for i in json_data:
        if "server" in i:
            server_list.append([i,json_data[i]])
    print(server_list)
    print(len(server_list))