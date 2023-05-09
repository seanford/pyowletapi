from src.pyowletapi.api import OwletAPI
from src.pyowletapi.sock import Sock
from src.pyowletapi.exceptions import OwletAuthenticationError, OwletConnectionError

import asyncio
import json


async def run():
    with open("login.json") as file:
        data = json.load(file)
    username = data['username']
    password = data['password']
    
    api = OwletAPI('europe', username, password)

    try:
        print(await api.authenticate())
        devices = await api.get_devices()

        socks = {device['device']['dsn']: Sock(api, device['device']) for device in devices}
        print(socks)
        #for i in range(10):
        for sock in socks.values():
            properties = await sock.update_properties()
            #properties = properties[1]
            print(properties[0])
            #print(properties['heart_rate'], properties['oxygen_saturation'], properties['battery_percentage'])   
    except (OwletAuthenticationError, OwletConnectionError) as err:
        print(err)

    await asyncio.sleep(60)
    await api.close()

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
