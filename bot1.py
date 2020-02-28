import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter
from discord import Spotify
import urllib.parse, urllib.request, re
import time
import pyowm
from flask import Flask
app = Flask(__name__)

@app.route("/")
client = commands.Bot(command_prefix='.')

converter = MemberConverter()

owm = pyowm.OWM('aab4feb1d7ca6a11a8fe49a0a8cfa0b0') #pyown api key

#267776835591340032 brandons discord id
#326191223301734401 my discord id
#254000877180944385 lucian discord id

@client.event
async def on_ready():
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Spotify'))
    print('Bot is ready')

def setup(client, ctx, user):
    client.add_cog(MyCog(client, ctx, user))

class MyCog(commands.Cog): #full code of this sent to sandra
    def __init__(self, client, ctx, user):
        self.client = client
        self.ctx = ctx
        self.user = user
        self.statusupdate.start()

    def cog_unload(self):
        self.statusupdate.cancel()

    @tasks.loop(seconds=5.0)
    async def statusupdate(self): #make listening status update
        user = self.user or self.ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=f'{activity.title} by ' + str(f'{activity.artist}').replace(';', ',')))

    @statusupdate.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.client.wait_until_ready()

@client.event
async def on_message(message):
    #a = message.guild.members
    #print(a)
    #print(message.author.id)
    if message.author.id == 267776835591340032:
        await message.channel.send('https://cdn.discordapp.com/attachments/365142031980560387/682059340508954702/image0.png')
    elif message.author.id == 254000877180944385:
        await message.channel.send('https://cdn.discordapp.com/attachments/365142031980560387/682064646039011580/cube_bruce.png')
    #elif message.author.id == 326191223301734401:
        #await message.channel.send('<@254000877180944385>')
    await client.process_commands(message)

@client.command()
async def startupspotify(ctx, user: discord.Member=None):
    setup(client, ctx, user)

@client.command()
async def status(ctx, member: discord.Member=None):
    await ctx.send(str(member.status))

@client.command()
async def spotify(ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            #print({activity.artist})
            #print(user.id)
            await ctx.send(f'<@{user.id}> is listening to {activity.title} by ' + str(f'{activity.artist}').replace(';',','))
            #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{activity.title} by ' + str(f'{activity.artist}').replace(';',',')))

def spotifyupdate(ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            return client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{activity.title} by ' + str(f'{activity.artist}').replace(';',',')))

@client.command()
async def msguser(ctx, member : discord.Member, *, message):
    await member.send(message)

@client.command()
async def msgnoob(ctx, message):
    member = await converter.convert(ctx, 'Maniacked#7370') #converts str to Member
    await member.send(message)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def brandon(ctx):
    #print(ctx.author.id)
    await ctx.send('is gay')

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)

@client.command()
async def dm(ctx):
    await ctx.author.send('cube ruse says hi')

@client.command()
async def yo(ctx):
    await ctx.author.send('shut up nigga')

@client.command()
async def pic(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/679524001285931040/679531125248622616/3c770a107f658a9b7760e6950aa4c32d.png')

@client.command()
async def weather(ctx, city): #town is same as city
    town = city.capitalize()
    try:
        city = owm.weather_at_place(city)
        w = city.get_weather()
        await ctx.send(ctx.author.mention + ', the current weather in ' + town + ' is ' + str(w.get_temperature('celsius')['temp']) + '°C' + ' with a forcast of ' + str(w.get_detailed_status()) + '.')
    except:
        await ctx.send(ctx.author.mention + ', that is not a valid city.')

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, * , search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    await ctx.send(':musical_note: Now Playing: ' + 'https://www.youtube.com/watch?v=' + search_results[0])

# def check_queue(id):
#     if queues[id] != []:
#         player = queues[id].pop(0)
#         players[id] = player
#         player.start()
#
# @client.command(pass_context=True)
# async def play(ctx, url):
#     server = ctx.guild
#     voice_client = ctx.voice_client
#     player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id)) #t0do fix
#     players[server.id] = player
#     player.start()
#
# @client.command(pass_context=True)
# async def queue(ctx, url):
#     server = ctx.message.guild
#     voice_client = client.voice_clients(server)
#     player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
#
#     if server.id in queues:
#         queues[server.id].append(player)
#     else:
#         queues[server.id] = [player]
#     await client.say('Video queued.')
#
#
# @client.command(pass_context=True)
# async def pause(ctx):
#     id = ctx.message.server.id
#     players[id].pause()
#
#
# @client.command(pass_context=True)
# async def stop(ctx):
#     id = ctx.message.server.id
#     players[id].stop()
#
#
# @client.command(pass_context=True)
# async def resume(ctx):
#     id = ctx.message.server.id
#     players[id].resume()

# @client.command(pass_context = True)
# async def play(ctx, url):
#     server = ctx.message.guild
#     voice_client = ctx.voice_client(server)
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()

# @client.command(pass_context = True)
# async def dmall(ctx, member : discord.Member = None, *, message):
#     if not ctx.message.author.server_permissions.administrator:
#         return
#     if not member:
#         return await client.say(ctx.message.author.mention + "Specify a user to DM!")
#     if member == "@everyone":
#         for server_member in ctx.message.server.members:
#             await client.send_message(server_member, message)
#     else:
#         await client.send_message(member, message)

# @client.event
# async def on_message(message):
#     if message.content.find('!guillau') != -1:
#         await message.send('noob')

# @client.command()
# async def dm(ctx):
#     await ctx.author.send(choice(quickList))

# @client.command()
# async def getpasswordtoken(ctx):
#     await ctx.send('password token for @etacsinmeL #9498 is: Njc1MRg1NzQ53jIxNTc2NjIy.XjzdxQ.B7BUjEhmOEMtVs3SvLNv4p-uw6D')

client.run('Njc5ODg4NjczODY0Njc5NDk2.Xlhi-Q.2y0pa3lRZ1WctIKiaTxsqAxI4Aw')
