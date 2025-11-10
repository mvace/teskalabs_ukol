import json
import aiofiles
from datetime import datetime, timezone
from models import Container


# Načíst data
async def load_data(file):
    async with aiofiles.open(file, mode="r") as f:
        data = await f.read()
    return json.loads(data)


# vytvořit instanci modelu Container, který bude obsahovat vyparsovaná data z json k jednotlivým kontejnerům
async def parse_container_data(container):
    name = container.get("name")
    created_at = container.get("created_at")
    status = container.get("status")
    cpu_usage = None
    memory_usage = None
    ip_addresses = []

    state = container.get("state")
    if state:
        cpu_usage = container.get("cpu_usage")
        memory_usage = container.get("memory_usage")
        network = state.get("network", [])
        for device_details in network.values():
            for ip_addr_info in device_details["addresses"]:
                ip_addresses.append(ip_addr_info["address"])

    return Container(
        name=name,
        created_at=created_at,
        status=status,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        ip_addresses=ip_addresses,
    )

