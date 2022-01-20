#!/usr/bin/python3

from asyncio import new_event_loop as loop
from logging import basicConfig, INFO

from bot_instance import BotInstance

if __name__ == "__main__":
    basicConfig(level=INFO)
    client = BotInstance(loop())
    try:
        task = loop().create_task(client.startup())
        loop().run_until_complete(task)
        loop().run_forever()
    except (KeyboardInterrupt, RuntimeError):
        print(f"Shutting down - {client.kill()}")
    except Exception as ex:
        print(f"Error - {ex}")
    finally:
        loop().close()
