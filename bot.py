from discord.colour import Colour
from scraper import Scraper
import discord
import asyncio
import datetime


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scraper = Scraper()
        self.factions_bg_task = self.loop.create_task(self.scrap_factions())
        self.turfs_bg_task = self.loop.create_task(self.scrap_turfs())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def scrap_factions(self):
        async def create_message(data):
            embed = discord.Embed(title="👉🏻 Statusul Aplicatiilor in Factiuni 👈🏻", 
                                url="https://www.rpg2.b-zone.ro/factions/index",
                                description=f"⏰ Ultima data actualizat la {datetime.datetime.now()} ⏰",
                                color=0x00ff62)
            embed.set_author(name="Danix43", icon_url="https://cdn.discordapp.com/avatars/783680772014997546/92a2a4d507b520d27aa91121a8dece50.png")
            embed.set_thumbnail(url="http://i.imgur.com/Z3UHdYS.png")
            for k, v in data.items():
                embed.add_field(name=k, value=v, inline=False)
            return embed

        while True:
            await self.wait_until_ready()
            data = await self.scraper.check_factions()
            print("sending message")
            await client.get_channel(813881450423386142).send(embed=await create_message(data))
            print("done, waiting")
            await asyncio.sleep(3600)
            print("done waiting, resuming")
    
    async def scrap_turfs(self):
        async def create_message(data):
            embed = discord.Embed(title="👉🏻 Situatia turfurilor in mafii 👈🏻", 
                                url="https://www.rpg2.b-zone.ro/wars/turfs",
                                description=f"⏰ Ultima data actualizat la {datetime.datetime.now()} ⏰",
                                color=0x00ff62)
            embed.set_author(name="Danix43", icon_url="https://cdn.discordapp.com/avatars/783680772014997546/92a2a4d507b520d27aa91121a8dece50.png")
            embed.set_thumbnail(url="http://i.imgur.com/Z3UHdYS.png")
            for k, v in data.items():
                embed.add_field(name=k, value=v, inline=False)
            return embed
        await self.wait_until_ready()
        data = await self.scraper.check_turfs()
        print("sending message")
        await client.get_channel(813881497525289031).send(embed=await create_message(data))
        print("done, waiting")
        await asyncio.sleep(86400)
        print("done waiting, resuming")


intents = discord.Intents.default()
intents.members = True


client = MyClient(intents=intents)
client.run('ODEzMzM0NDU2MDU1NjI3Nzc2.YDNyvQ.LZQ4Qfloi3mvQwbkN2Ln64EPl80')

if __name__ == "__main__":
    MyClient()