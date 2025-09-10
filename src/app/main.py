import asyncio

from app.config import Settings


async def run():
    Settings.load()
    # TODO: build DI graph: repo, usecases, adapters, controller, scheduler
    print("Stub main. Configure DI in this file.")


if __name__ == "__main__":
    asyncio.run(run())
