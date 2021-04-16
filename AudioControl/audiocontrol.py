from redbot.core import commands, Config
from redbot.core.utils import AsyncIter
from redbot.core.errors import RedError
from redbot.cogs.audio.core.cog_utils import PlaylistConverter #https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/converters.py
from redbot.cogs.audio.converters import ScopeParser #https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/converters.py
from redbot.cogs.audio.apis.playlist_interface import get_all_playlist_converter, get_all_playlist #https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/apis/playlist_interface.py
import copy
import asyncio
import string
import random
import discord

"""
This is only an RPC handler for the built-in Audio module of RED located here:
https://github.com/Cog-Creators/Red-DiscordBot/tree/V3/develop/redbot/cogs/audio
All credits go to RED devs

Permissions and checks are handled by the Audio cog
    - This cog does nothing but creating a custom Context class using an api key which
      allows you to interact with the Audio module via RPC

This is not officially supported/maintained by the team of the Audio cog
thus features can break.

You can always reach me on discord: Benno#8969
"""

class InvalidAPIKeyError(RedError):
    """Raised when an invalid API key is given"""

class InvalidScopeError(RedError):
    """Raised when the passed scope is invalid"""

class AudioControl(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, identifier=163274234)
        self.audio = self.bot.get_cog("Audio")

        default_guild = {
            "music_channel": None
        }
        default_apikey = {
            "user_id": None,
            "guild_id": None
        }

        self.config.register_guild(**default_guild)
        self.config.init_custom("apikey", 1)
        self.config.register_custom("apikey", **default_apikey)

    async def get_ctx(self, apikey, command):
        """constructs a custom commands.Context class by spoofing a message
        Thanks Jack and Draper"""
        apikey_values = await self.config.custom("apikey", apikey).all()
        user_id = apikey_values["user_id"]
        guild_id = apikey_values["guild_id"]

        if (user_id == None) or (guild_id == None):
            raise InvalidAPIKeyError("Guild or user ID not found")

        msg = copy.copy(self.bot.cached_messages[0])
        prefix = self.bot.command_prefix
        msg.content = f"{prefix}{command}"

        for guild in self.bot.guilds:
            if guild.id == guild_id:
                break
        else:
            raise InvalidAPIKeyError("Guild is not available anymore")

        msg.channel = discord.utils.get(guild.channels, id=await self.config.guild(guild).music_channel())
        msg.author = discord.utils.get(guild.members, id=user_id)

        ctx = await self.bot.get_context(msg)
        ctx.guild = guild
        ctx.command = self.bot.get_command(command)
        ctx.command.cog = self.audio
        return ctx

    async def generate_key(self, current_apikeys):
        while True:
            apikey = "".join(random.choice(string.ascii_letters + string.digits) for i in range(16))
            if apikey not in current_apikeys.keys():
                break
        return apikey

    async def play(self, apikey, title):
        """Plays a song
        Title: localpath, song name or url
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/controller.py"""
        ctx = await self.get_ctx(apikey, "play")
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_play(ctx, query=title)

    async def play_playlist(self, apikey, playlist):
        """Starts a playlist
        playlist can either be a name or ID
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/playlists.py"""
        ctx = await self.get_ctx(apikey, "playlist start")
        playlist = await PlaylistConverter.convert(self=self.audio, ctx=ctx, arg=playlist)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_playlist_start(ctx=ctx, playlist_matches=playlist)

    async def get_playlists(self, apikey, arg):
        ctx = await self.get_ctx(apikey, "playlist list")
        playlists = await get_all_playlist(
            scope=arg,
            bot=self.bot,
            playlist_api=self.audio.playlist_api,
            guild=ctx.guild,
            author=ctx.author
        )
        playlist_list = []
        space = "\N{EN SPACE}"
        async for playlist in AsyncIter(playlists):
            print(playlist)
            playlist_list.append(
                ("\n" + space * 4).join(
                    (
                        playlist.name,
                        f"ID: {playlist.id}",
                        f"Tracks: {len(playlist.tracks)}",
                        "Author: {name}".format(
                            name=self.bot.get_user(playlist.author)
                            or playlist.author
                            or "Unknown"),
                        f"Scope: {self.audio.humanize_scope(playlist.scope)}\n"
                    )
                )
            )
        return playlist_list

    async def volume(self, apikey, set_vol: int = None, change_vol: int = None):
        """Change the volume
        set_vol: set the volume to a given level
        change_vol: increase/decrease the volume by the given margin
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/controller.py"""
        ctx = await self.get_ctx(apikey, "volume")
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            if isinstance(set_vol, int):
                await self.audio.command_volume(ctx=ctx, vol=set_vol)
            elif (set_vol == None) and (change_vol == None):
                await self.audio.command_volume(ctx=ctx)
            else: 
                volume = await self.audio.config.guild(ctx.guild).volume()
                volume += change_vol
                await self.audio.command_volume(ctx=ctx, vol=volume)

    async def skip(self, apikey):
        """Skip the current song
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/controller.py"""
        ctx = await self.get_ctx(apikey, "skip")
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_skip(ctx)

    async def previous(self, apikey):
        """Return to the previous song
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/controller.py"""
        ctx = await self.get_ctx(apikey, "prev")
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_prev(ctx)

    async def pause(self, apikey):
        """Pause/resume the current song
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/controller.py"""
        ctx = await self.get_ctx(apikey, "pause")
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_pause(ctx)

    async def stop(self, apikey):
        """Stop the player
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/audio/core/commands/controller.py"""
        ctx = await self.get_ctx(apikey, "stop")
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_stop(ctx)

    @commands.guild_only()
    @commands.group(name="apikey")
    async def apikey(self, ctx):
        pass

    @commands.guild_only()
    @apikey.command(name="generate")
    async def apikey_generate(self, ctx):
        async with self.config.custom("apikey").all() as apikeys:
            for apikey, value in tuple(apikeys.items()):
                if (value["user_id"] == ctx.author.id) and (value["guild_id"] == ctx.guild.id):
                    del apikeys[apikey]

            apikey = await self.generate_key(apikeys)
            apikeys[apikey] = {"user_id": ctx.author.id, "guild_id": ctx.guild.id}
            await ctx.author.send(f"Your API key for AudioControl RPC is:\n`{apikey}`")

    @commands.guild_only()
    @apikey.command(name="show")
    async def apikey_show(self, ctx):
        apikeys = await self.config.custom("apikey").get_raw()
        for apikey, value in apikeys.items():
            if (value["user_id"] == ctx.author.id) and (value["guild_id"] == ctx.guild.id):
                await ctx.author.send(f"Your API key for AudioControl RPC is:\n`{apikey}`")
                break

    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command(name="musicchannel")
    async def musicchannel(self, ctx, channel: discord.TextChannel):
        await self.config.guild(ctx.guild).music_channel.set(channel.id)
        await ctx.send(f"RPC audio commands will now be sent to {channel.mention}")

    @commands.command(name="testac")
    async def testac(self, ctx, scope = ""):
        print(await self.get_playlists(apikey="PKVQeYldZxgVBBZm", arg="", scope=scope))
