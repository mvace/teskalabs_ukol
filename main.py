import json
import asyncio
import aiofiles
from datetime import datetime, timezone
from models import Container
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session_factory, engine


# Načíst data
async def load_data(file):
    async with aiofiles.open(file, mode="r") as f:
        data = await f.read()
    return json.loads(data)


# vytvořit instanci modelu Container, který bude obsahovat vyparsovaná data z json k jednotlivým kontejnerům
async def parse_container_data(container):
    name = container.get("name")
    date_string = container.get("created_at")
    dt = datetime.fromisoformat(date_string)
    created_at = int(dt.timestamp())

    status = container.get("status")
    cpu_usage = None
    memory_usage = None
    ip_addresses = []

    state = container.get("state")
    if state:
        cpu_usage = state.get("cpu").get("usage")
        memory_usage = state.get("memory").get("usage")
        network = state.get("network", {})
        for device_details in network.values():
            addresses = device_details.get("addresses", [])
            for ip_addr_info in addresses:
                address = ip_addr_info.get("address")
                ip_addresses.append(address)

    return Container(
        name=name,
        created_at=created_at,
        status=status,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        ip_addresses=ip_addresses,
    )


# Načtení dat ze souboru, naparsování na Container objekty, hromadné uložení do databáze
async def process_and_prepare_data(session, filepath):
    raw_data_list = await load_data(filepath)
    containers_to_add = []
    for data in raw_data_list:
        new_container = await parse_container_data(data)
        containers_to_add.append(new_container)

    session.add_all(containers_to_add)


async def main():

    async with async_session_factory() as session:
        async with session.begin():
            await process_and_prepare_data(session, "sample-data.json")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
