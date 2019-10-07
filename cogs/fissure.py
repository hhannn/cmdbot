import requests
import json
import asyncio
import discord
from discord.ext import commands

class Fissure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.fissure())

    @commands.Cog.listener()
    async def on_ready(self):
        print("fissure bot is online")

    async def fissure(self):
        await self.bot.wait_until_ready()

        channel=self.bot.get_channel(629082481395761153)

        while not self.bot.is_closed():
            response=requests.get('https://api.warframestat.us/pc/fissures')

            embed=discord.Embed(colour=discord.Colour(0xd4bf53))

            embed.set_thumbnail(url="https://i.imgur.com/b4jshCx.png")
            embed.set_author(name="Void Fissures")

            for key in response.json():
                eta=''
                if '-' in key['eta']:
                    eta='Expired'
                else:
                    eta=f"Ends in {key['eta']}"
                embed.add_field(
                    name=f"{key['node']} - T{key['tierNum']}",
                    value=f"{key['missionType']} - {key['enemy']}\n{key['tier']} Fissure\n__{eta}__"
                )
            await channel.send(embed=embed, delete_after=29.0)
            await asyncio.sleep(30)

def setup(bot):
    bot.add_cog(Fissure(bot))