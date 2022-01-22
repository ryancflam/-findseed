from asyncio import new_event_loop as loop
from logging import StreamHandler, getLogger, INFO
from sys import stdout

from bot_instance import BotInstance

if __name__ == "__main__":
    handler = StreamHandler(stream=stdout)
    handler.setLevel(INFO)
    getLogger().addHandler(handler)
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
