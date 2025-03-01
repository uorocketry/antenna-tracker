#AsyncTest


import asyncio
import time
from AsyncAntenna import Antenna

async def say_after(what):
    #await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")
    antenna = Antenna(47.98714, -81.84864, 62.52301, False, "IDLE") #STEM

    await antenna.move_tracker(90,90)
    await say_after('world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())