import os
import json
import requests
import discord
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
import asyncio

bot = commands.Bot(command_prefix = '!')

bot.remove_command('help')

@bot.event
async def on_ready():
    print('cmd bot is online')

async def changepr():
    await bot.wait_until_ready()
    channel = bot.get_channel(624999751674232869)
    counter = 0
    while not bot.is_closed():
        cetus_req=requests.get('https://api.warframestat.us/pc/cetusCycle')
        vallis_req=requests.get('https://api.warframestat.us/pc/vallisCycle')
        cetus_time=cetus_req.json()['shortString']
        vallis_time=vallis_req.json()['shortString']
        url='https://hub.warframestat.us/#/'
        terry='https://vignette.wikia.nocookie.net/warframe/images/7/73/Teralyst.png/revision/latest?cb=20171016171720'
        if cetus_time.endswith('Day'):
            cetus_time = cetus_time.replace('Day', '🌞')
        else:
            cetus_time = cetus_time.replace('Night', '🌙')
        if vallis_time.endswith('Warm'):
            vallis_time = vallis_time.replace('Warm', '🔥')
        else:
            vallis_time = vallis_time.replace('Cold', '❄️')
        await bot.change_presence(activity=discord.Game(name=f"{cetus_time} | {vallis_time}"))
        if cetus_time.startswith('20m to Night') and counter == 0:
            embed=discord.Embed(title="Cetus Notification", url=url, color=0x22fe1d)
            embed.set_thumbnail(url=terry)
            embed.add_field(name='20m to Night', value='@everyone the remnants of massive Sentients is about to rise.', inline=True)
            await channel.send(embed=embed, delete_after = 60.0)
            counter += 1
            print(counter)
        elif cetus_time.startswith('10m to Night') and counter == 1:
            embed=discord.Embed(title="Cetus Notification", url=url, color=0x22fe1d)
            embed.set_thumbnail(url=terry)
            embed.add_field(name='10m to Night', value='@everyone can you hear the Eidolon howling?', inline=True)
            embed.set_footer(text='"And now, a massive Sentient energy spike in your area. I advise you to be careful."')
            await channel.send(embed=embed, delete_after = 60.0)
            counter = 0
        await asyncio.sleep(15)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
@has_permissions(manage_messages = True)
async def purge(ctx, amount : int):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} amount of messages.", delete_after=10.0)
        
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.channel.send(f'{ctx.message.author.mention} says {message}.')

bot.load_extension('cogs.fissure')
bot.load_extension('cogs.muhbot')

bot.loop.create_task(changepr())
bot.run('NjI0OTkyMjI2NzI3OTUyMzk1.XYZDXg.g6vJ97WIq1KiG8YYv6n-QtFP-Sk')