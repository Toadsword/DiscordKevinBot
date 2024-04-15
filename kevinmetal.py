# This example requires the 'message_content' privileged intent to function.
import asyncio
import discord
import time
import random
import threading

from discord.ext import commands
from os import listdir
from os.path import isfile, join
allSounds = [f for f in listdir("./sounds") if isfile(join("./sounds", f))]

minTime = 15
maxTime = 180


class Kevin(commands.Cog):
    vClient = None
    treadStarted = False
    thread = None

    def __init__(self, bot):
        self.bot = bot
        treadStarted = False
        print('__init__ Kevin')
        

    @commands.command()
    async def kevin(self, ctx):
        print(self.treadStarted)
        if not self.treadStarted:
            self.treadStarted = True
            self.playSound()

    @commands.command()
    async def stop(self, ctx):
        print('stop')
        """Stops and disconnects the bot from voice"""
        self.thread.cancel()
        await ctx.voice_client.disconnect()

    @kevin.before_invoke
    async def ensure_voice(self, ctx):
        print("ensuring invoke")
        if ctx.voice_client is None:
            if ctx.author.voice:
                self.vClient = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            
    def playSound(self):
        soundNumber = random.randrange(0, len(allSounds) - 1)
        print(f'played sound {soundNumber}')
        if self.vClient.is_playing():
            self.thread = threading.Timer(3, self.playSound).start()
            return

        source = discord.FFmpegOpusAudio(f'sounds/{allSounds[soundNumber]}')
        self.vClient.play(source)
        if self.vClient.is_connected():
            delay = random.randrange(minTime, maxTime)
            print(f"Next sound in : {delay}")
            self.thread = threading.Timer(delay, self.playSound).start()



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or("!"),
    description = 'Typical kevin behavior',
    intents=intents,
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f"loaded {len(allSounds)} sounds")
    print(allSounds)
    print('------')


async def main(token):
    async with bot:
        await bot.add_cog(Kevin(bot))
        await bot.start(token)

def runBot(token):
    asyncio.run(main(token))