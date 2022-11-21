import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
intents = discord.Intents.default()
intents.members = True

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix = '*')

@client.event
async def on_ready():
    print("The bot is at your service!")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")

@client.command()
async def hello(ctx):
    await ctx.send("Hey, this is Leviathan.")

@client.command()
async def bye(ctx):
    await ctx.send("Bye, smooth sailin' sailor!")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(['1. Audio1.wav', '2. Audio2.wav', '3. Audio3.wav',
                                 '4. Audio4.wav', '5. Audio5.wav', '6. Audio6.wav', '7. Audio7.wav'])
        player = voice.play(source)

    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Au revoir!")
    else:
        await ctx.send("I am not in a voice channel.")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("I am not playing any audio on the Voice Channel currently")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("At the moment, no audio is paused.")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.wav')
    player = voice.play(source, after = lambda x = None: check_queue(ctx, ctx.message.guild.id))
    print(arg)

@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.wav')
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]
    await ctx.send("Added to queue.")

client.run("OTM2MTU4MTgxMTY2NTc1NjM3.YfJHPw.5sWDEKx6dtQSd8fiFxzLpqGEcis")
