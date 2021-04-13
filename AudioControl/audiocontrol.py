from redbot.core import commands
from redbot.cogs.audio.core.cog_utils import PlaylistConverter
from redbot.cogs.audio.converters import ScopeParser
import copy
import asyncio

class AudioControl(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.audio = self.bot.get_cog("Audio")
        asyncio.create_task(self.get_ctx())

    async def get_ctx(self):
        for msg in self.bot.cached_messages:
            ctx = await self.bot.get_context(msg)
            if ctx.cog != None:
                if ctx.cog.qualified_name == "Audio":
                    #print(ctx.cog.qualified_name)
                    self.ctx = ctx
                    return
        
        if self.ctx == None:
            raise ValueError("Issue an audio command first.")

    async def play(self, title):
        ctx = self.ctx
        await self.audio.command_play(ctx, query=title)

    async def play_playlist(self, playlist):
        ctx = self.ctx
        playlist = await PlaylistConverter.convert(self=self.audio, ctx=ctx, arg=playlist)
        await self.audio.command_playlist_start(ctx=ctx, playlist_matches=playlist)

    async def get_playlists(self):
        #scope = await ScopeParser.convert(self=self.audio, ctx=self.ctx, argument=)
        await self.audio.command_playlist_list(ctx=self.ctx)

    async def volume(self):
        await self.audio.command_volume(ctx=self.ctx)

    async def volume_up(self):
        volume = await self.audio.config.guild(self.ctx.guild).volume()
        volume = volume + 1
        await self.audio.command_volume(ctx=self.ctx, vol=volume)

    async def volume_down(self):
        volume = await self.audio.config.guild(self.ctx.guild).volume()
        volume = volume - 1
        await self.audio.command_volume(ctx=self.ctx, vol=volume)

    async def skip(self):
        await self.audio.command_skip(self.ctx)

    async def previous(self):
        await self.audio.command_prev(self.ctx)

    async def pause(self):
        await self.audio.command_pause(self.ctx)

    async def stop(self):
        await self.audio.command_stop(self.ctx)

    @commands.command(name="reloadctx")
    async def testad(self, ctx):
        self.ctx = await self.get_ctx()
    # async def audiocontrol_task(self)s