import json
from datetime import datetime, timezone

# Načíst data

with open("sample-data.json", "r") as file:
    data = json.load(file)

# vytvořit seznam, který bude obsahovat slovník s požadovanými daty k danému kontejneru
container_list = []

for container in data:
    container_dict = {}
    container_dict["name"] = container["name"]

    container_dict["created_at"] = container["created_at"]
    container_dict["status"] = container["status"]

    ip_addresses = []

    # Ne vždy jsou data ve "state" přítomna a klíče "cpu" či "memory" chybí
    if container["state"] is None:
        container_dict["cpu_usage"] = None
        container_dict["memory_usage"] = None
    else:
        container_dict["cpu_usage"] = container["state"]["cpu"]["usage"]
        container_dict["memory_usage"] = container["state"]["memory"]["usage"]

        for device_name, device_details in container["state"]["network"].items():
            for data in device_details["addresses"]:
                ip_addresses.append(data["address"])

    container_dict["ip_addresses"] = ip_addresses
    container_list.append(container_dict)

for container in container_list:
    print(container)
