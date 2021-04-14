from redbot.core import commands, Config
from redbot.cogs.audio.core.cog_utils import PlaylistConverter
from redbot.cogs.audio.converters import ScopeParser
import copy
import asyncio
import string
import random
import discord

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

    async def get_ctx(self, apikey):
        apikey_values = await self.config.custom("apikey", apikey).all()
        user_id = apikey_values["user_id"]
        guild_id = apikey_values["guild_id"]

        msg = copy.copy(self.bot.cached_messages[0])
        msg.content = "!play"

        for guild in self.bot.guilds:
            if guild.id == guild_id:
                #msg.guild = guild
                break

        msg.channel = discord.utils.get(guild.channels, id=await self.config.guild(guild).music_channel())
        msg.author = discord.utils.get(guild.members, id=user_id)

        ctx = await self.bot.get_context(msg)
        ctx.guild = guild
        return ctx

    async def play(self, apikey, title):
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_play(ctx, query=title)

    async def play_playlist(self, apikey, playlist):
        ctx = await self.get_ctx(apikey)
        playlist = await PlaylistConverter.convert(self=self.audio, ctx=ctx, arg=playlist)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_playlist_start(ctx=ctx, playlist_matches=playlist)

    async def get_playlists(self, apikey):
        #scope = await ScopeParser.convert(self=self.audio, ctx=ctx, argument=)
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_playlist_list(ctx=ctx)

    async def volume(self, apikey):
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_volume(ctx=ctx)

    async def volume_up(self, apikey):
        ctx = await self.get_ctx(apikey)
        volume = await self.audio.config.guild(ctx.guild).volume()
        volume = volume + 1
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_volume(ctx=ctx, vol=volume)

    async def volume_down(self, apikey):
        ctx = await self.get_ctx(apikey)
        volume = await self.audio.config.guild(ctx.guild).volume()
        volume = volume - 1
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_volume(ctx=ctx, vol=volume)

    async def skip(self, apikey):
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_skip(ctx)

    async def previous(self, apikey):
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_prev(ctx)

    async def pause(self, apikey):
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_pause(ctx)

    async def stop(self, apikey):
        ctx = await self.get_ctx(apikey)
        if not (await self.config.guild(ctx.guild).music_channel()) == None:
            await self.audio.command_stop(ctx)

    async def generate_key(self, current_apikeys):
        while True:
            apikey = "".join(random.choice(string.ascii_letters + string.digits) for i in range(16))
            if apikey not in current_apikeys.keys():
                break
        return apikey

    @commands.guild_only()
    @commands.group(name="apikey")
    async def apikey(self, ctx):
        pass

    @commands.guild_only()
    @apikey.command(name="generate")
    async def apikey_generate(self, ctx):
        apikeys = await self.config.custom("apikey").get_raw()

        for apikey, value in tuple(apikeys.items()):
            if (value["user_id"] == ctx.author.id) and (value["guild_id"] == ctx.guild.id):
                del apikeys[apikey]

        apikey = await self.generate_key(apikeys)
        apikeys[apikey] = {"user_id": ctx.author.id, "guild_id": ctx.guild.id}
        await self.config.custom("apikey").set_raw(value=apikeys)
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


