# This example requires the 'message_content' privileged intent to function.
import asyncio
import discord
import time
import random
import threading

from discord.ext import commands
from os import listdir
from os.path import isfile, join

minTime = 15
maxTime = 180
soundspath = "./sounds/"


class Kevin(commands.Cog):
    #Global vars
    vClient = None
    thread = None
    allSounds = None
    treadStarted = False

    def __init__(self, bot):
        self.bot = bot
        print('__init__ Kevin')
        
    # Commands
    @commands.command()
    async def kevin(self, ctx):
        print(self.treadStarted)
        if not self.treadStarted:
            self.refreshsounds()
            self.treadStarted = True
            self.playSound()
            await ctx.send("J'arrive !")

    @commands.command()
    async def true_help(self, ctx):
        await ctx.send("Alors : \n $help : Affiche ce mess'\n $kevin : J'viens vous tenir companie dans le voice chat\n $addsound : Ajoute + de bonheur dans mon soundboard. T'faut link un son en pièce jointe !\n $daronned : J'pense t'as pas besoin d'explication...")


    @commands.command()
    async def addsound(self, ctx):
        message = ctx.message.content
        if str(ctx.message.attachments) == "[]": # Checks if there is an attachment on the message
            await ctx.send("J'aurais p't'etre b'soin que tu me mette en pièce jointe un son frr")
            return
        else: # If there is it gets the filename from message.attachments
            split_v1 = str(ctx.message.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            if filename.endswith(".mp3") or filename.endswith(".ogg"): # Checks if it is a .mp3 or ogg file
                await ctx.message.attachments[0].save(fp="sounds/{}".format(filename)) # saves the file
                await ctx.send("Ayé j'l'ai")
                self.refreshsounds()
            

    @commands.command()
    async def daronned(self, ctx):
        print('stop')
        """Stops and disconnects the bot from voice"""
        if self.thread.is_alive():
            self.thread.cancel()
        await ctx.send("ça va j'ai compris :unamused:")
        await ctx.voice_client.disconnect()

    @kevin.before_invoke
    async def ensure_voice(self, ctx):
        print("ensuring invoke")
        if ctx.voice_client is None:
            if ctx.author.voice:
                self.vClient = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("oooh connecte toiiiii.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    # Utility 
    def playSound(self):
        soundNumber = random.randrange(0, len(self.allSounds) - 1)
        print(f'played sound {soundNumber}')
        if self.vClient.is_playing():
            self.thread = threading.Timer(3, self.playSound).start()
            return

        source = discord.FFmpegOpusAudio(f'sounds/{self.allSounds[soundNumber]}')
        self.vClient.play(source)
        if self.vClient.is_connected():
            delay = random.randrange(minTime, maxTime)
            print(f"Next sound in : {delay}")
            self.thread = threading.Timer(delay, self.playSound).start()

    def refreshsounds(self):
        self.allSounds = [f for f in listdir(soundspath) if isfile(join(soundspath, f))]


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or("$"),
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