import asyncio
from aiohttp_json_rpc import JsonRpcClient
import keyboard

url = "10.0.0.93"
apikey = "PKVQeYldZxgVBBZm"
port = "6001"

async def rpc_handler_aiohttp(function, params = {}):
    try:
        print(f"Sent to {function}")
        rpc_client = JsonRpcClient()
        try:
            await rpc_client.connect(url, port)
            await rpc_client.call(method=function, params=params)
        finally:
            await rpc_client.disconnect()
    except asyncio.exceptions.TimeoutError:
        pass

keyboard.add_hotkey("ctrl+7", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__PLAY_PLAYLIST", {"apikey": apikey, "playlist": "OldButGold"})))
keyboard.add_hotkey("ctrl+1", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__STOP", {"apikey": apikey})))
keyboard.add_hotkey("ctrl+4", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__PREVIOUS", {"apikey": apikey})))
keyboard.add_hotkey("ctrl+6", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__SKIP", {"apikey": apikey})))
keyboard.add_hotkey("ctrl+8", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME", {"apikey": apikey, "change_vol": 2})))
keyboard.add_hotkey("ctrl+2", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME", {"apikey": apikey, "change_vol": -2})))

keyboard.wait()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PLAY", {"apikey": apikey, "title": "Hello"}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PLAY_PLAYLIST", {"apikey": apikey, "playlist": "OldButGold"}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__GET_PLAYLISTS", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__STOP", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PAUSE", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__SKIP", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PREVIOUS", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME", {"apikey": apikey, "set_vol": 10}))
