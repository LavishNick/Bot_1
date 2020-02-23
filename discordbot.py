import discord
from discord.ext import commands
import youtube_dl
import nacl.utils
import urllib.parse, urllib.request, re

client = commands.Bot(command_prefix='.')

players = {}
queues = {}

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def brandon(ctx):
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

client.run('Njc5ODg4NjczODY0Njc5NDk2.XlBxIw.HEWpdKFSnurxZL6H0YusXqGOvjg')
