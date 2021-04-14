import asyncio
from aiohttp_json_rpc import JsonRpcClient
import keyboard

url = "localhost"
apikey = "your-api-key-here"

def exception_catching_callback(task):
    if task.exception():
        task.print_stack()

async def rpc_handler_aiohttp(function, params = {}):
    try:
        print(f"Sent to {function}")
        rpc_client = JsonRpcClient()
        try:
            await rpc_client.connect(url, "6133")
            await rpc_client.call(method=function, params=params)
        finally:
            await rpc_client.disconnect()
    except asyncio.exceptions.TimeoutError:
        pass

# keyboard.add_hotkey("7", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__PLAY_PLAYLIST", {"playlist": "OldButGold"})))
# keyboard.add_hotkey("1", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__STOP")))
# keyboard.add_hotkey("8", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME_UP")))
# keyboard.add_hotkey("2", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME_DOWN")))
# keyboard.add_hotkey("4", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__PREVIOUS")))
# keyboard.add_hotkey("6", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__SKIP")))
# keyboard.add_hotkey("9", lambda: asyncio.run(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME")))

# keyboard.wait("esc")

loop = asyncio.get_event_loop()
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PLAY", {"apikey": apikey, "title": "Hello"}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PLAY_PLAYLIST", {"apikey": apikey, "playlist": "OldButGold"}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__GET_PLAYLISTS", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__STOP", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PAUSE", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__SKIP", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__PREVIOUS", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME_UP", {"apikey": apikey}))
# loop.run_until_complete(rpc_handler_aiohttp("AUDIOCONTROL__VOLUME_DOWN", {"apikey": apikey}))
