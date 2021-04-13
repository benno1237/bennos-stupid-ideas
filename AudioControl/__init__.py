from .audiocontrol import AudioControl

def setup(bot):
    cog = AudioControl(bot)
    bot.add_cog(cog)

    bot.register_rpc_handler(cog.play)
    bot.register_rpc_handler(cog.play_playlist)
    bot.register_rpc_handler(cog.get_playlists)
    bot.register_rpc_handler(cog.stop)
    bot.register_rpc_handler(cog.volume)
    bot.register_rpc_handler(cog.volume_down)
    bot.register_rpc_handler(cog.volume_up)
    bot.register_rpc_handler(cog.skip)
    bot.register_rpc_handler(cog.previous)
    bot.register_rpc_handler(cog.pause)