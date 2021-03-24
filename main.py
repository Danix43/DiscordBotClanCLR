import discord
import asyncio
import pytz
import os

from scraper import Scraper
from datetime import time, datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tz = pytz.timezone("Europe/Bucharest")
        self.scraper = Scraper()
        self.factions_bg_task = self.loop.create_task(self.scrap_factions())
        self.turfs_bg_task = self.loop.create_task(self.run_at(time(22, 00, tzinfo=self.tz), self.scrap_turfs()))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def wait_until(self, time_to_run):
        now = time.now()
        await asyncio.sleep((time_to_run - now).total_seconds())

    async def run_at(self, time_to_run, coro):
        await self.wait_until(time_to_run)
        return await coro


    async def create_embed_info(self, title, link, data):
        embed = discord.Embed(title=title, 
                                url=link,
                                description=f"⏰ Ultima data actualizat la {datetime.now(self.tz)}⏰",
                                color=0x00ff62)
        embed.set_author(name="Danix43", icon_url="https://cdn.discordapp.com/avatars/783680772014997546/92a2a4d507b520d27aa91121a8dece50.png")
        embed.set_thumbnail(url="http://i.imgur.com/Z3UHdYS.png")
        for k, v in data.items():
            embed.add_field(name=k, value=v, inline=False)
        return embed

    async def on_message(self, message):
        async def create_embed():
            link_mapa = "http://bit.ly/3cilAMo"
            link_discord = "https://discord.gg/yeZGaTfWnK"
            
            embed = discord.Embed(title="Mod Mapa Pe M cu Locatiile B-Zone",
                                    description="Modul este inca in development, check for updates",
                                    color=0xfc0303)
            embed.set_author(name="Danix43", icon_url="https://cdn.discordapp.com/avatars/783680772014997546/92a2a4d507b520d27aa91121a8dece50.png")
            embed.set_thumbnail(url="http://i.imgur.com/Z3UHdYS.png")
            embed.add_field(name="Join Us", value=link_discord, inline=False)
            embed.add_field(name="Mod Link", value=link_mapa, inline=False)
            return embed

        if message.author == self.user:
            return

        if message.content == "mapa pe m":
            if message.channel.type == discord.ChannelType.private:
                await message.channel.send(embed=await create_embed())
            else:
                return

    async def scrap_factions(self):
        while True:
            await self.wait_until_ready()
            data = await self.scraper.check_factions()
            print("sending message")
            # dev channel
            # await client.get_channel(813745203680378890).send(
            #     embed=await self.create_embed_info("👉🏻 Statusul Aplicatiilor in Factiuni 👈🏻", 
            #                                 "https://www.rpg2.b-zone.ro/factions/index",
            #                                     data))            
            # prod channel
            await client.get_channel(813881450423386142).send(
                embed=await self.create_embed_info("👉🏻 Statusul Aplicatiilor in Factiuni 👈🏻", 
                                            "https://www.rpg2.b-zone.ro/factions/index",
                                                data))
            print("done scraping the factions")
            await asyncio.sleep(10800)
            

    async def scrap_turfs(self):
        await self.wait_until_ready()
        data = await self.scraper.check_turfs()
        print("sending message")
        # dev channel
        # await client.get_channel(813834934673735761).send(
        #     embed=await self.create_embed_info("👉🏻Situatia turfurilor in mafii👈🏻", 
        #                                     "https://www.rpg2.b-zone.ro/wars/turfs",
        #                                     data))
        # prod channel
        await client.get_channel(813881497525289031).send(
            embed=await self.create_embed_info("👉🏻Situatia turfurilor in mafii👈🏻", 
                                            "https://www.rpg2.b-zone.ro/wars/turfs",
                                            data))
        print("done scraping the turfs")


intents = discord.Intents.default()
intents.members = True


client = MyClient(intents=intents)
client.run(TOKEN)

if __name__ == "__main__":
    MyClient()