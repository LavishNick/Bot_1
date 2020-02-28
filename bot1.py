import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter
from discord import Spotify
import urllib.parse, urllib.request, re
import time
import pyowm

client = commands.Bot(command_prefix='.')

converter = MemberConverter()

owm = pyowm.OWM('aab4feb1d7ca6a11a8fe49a0a8cfa0b0') #pyown api key

@client.event
async def on_ready():
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

client.run('Njc5ODg4NjczODY0Njc5NDk2.Xlhi-Q.2y0pa3lRZ1WctIKiaTxsqAxI4Aw')
