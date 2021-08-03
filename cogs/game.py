import json

from asyncio import get_event_loop, sleep
from concurrent.futures import ThreadPoolExecutor

import discord
from discord.colour import Color
from discord.ext import commands

class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def game(self, ctx: commands.Context):
        """Join the actual game of  clash of code"""
        coc = await self.bot.codingame_client.get_pending_clash_of_code()
        embed = discord.Embed(
            title="Click to join", 
            url=coc.join_url, 
            description="**Players online:**", 
            color=Color.blue()
        )
        embed.set_thumbnail(
            url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png"
        )
        for player in coc.players:
            embed.add_field(
                name=player.pseudo, 
                value="[See profil](https://www.codingame.com/profile/" + player.public_handle + ")"
            )
        embed.set_footer(text="Time before start: " + str(coc.time_before_start.seconds) + "s")
        await ctx.send(embed=embed)

    @commands.command(name="next")
    async def nextgame(self, ctx: commands.Context):
        """Join the next game of clash of code"""
        coc = await self.bot.codingame_client.get_pending_clash_of_code()
        next_battle = coc.time_before_start.seconds
        msg = await ctx.send(f"Next battle in {next_battle} s ~")
        while next_battle > 5:
            coc = await self.bot.codingame_client.get_pending_clash_of_code()
            next_battle = coc.time_before_start.seconds
            await msg.edit(content=f"Next battle in {next_battle} s ~")
            await sleep(5)
        await sleep(next_battle + 5)
        await ctx.send(ctx.author.mention)
        coc = await self.bot.codingame_client.get_pending_clash_of_code()
        while not coc:
            coc = await self.bot.codingame_client.get_pending_clash_of_code()
            sleep(1)
        embed = discord.Embed(
            title="Click to join", 
            url=coc.join_url, 
            description="**Players online:**", 
            color=Color.blue()
        )
        embed.set_thumbnail(
            url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png"
        )
        for p in coc.players:
            embed.add_field(
                name=p.pseudo, 
                value=f"[See profil](https://www.codingame.com/profile/{p.public_handle})"
            )
        embed.set_footer(text=f"Time before start: {coc.time_before_start}")
        await ctx.send(embed=embed)

    @commands.command()
    async def profil(self, ctx: commands.Context, arg=None):
        """See an user profil from codingame"""
        if not arg:
            loop = get_event_loop()
            file_data = await loop.run_in_executor(ThreadPoolExecutor(), self._read_db)
            if str(ctx.author.id) not in file_data.keys():
                await ctx.send("if you provide no argument, please use !link first")
                return
            if not file_data[str(ctx.author.id)]["user"]:
                await ctx.send("if you provide no argument, please use !link first")
                return
            arg = file_data[str(ctx.author.id)]["user"]
        codingamer = await self.bot.codingame_client.get_codingamer(arg)
        embed = discord.Embed(
            title=codingamer.pseudo, 
            url=f"https://www.codingame.com/profile/{codingamer.public_handle}", 
            color=Color.orange()
        )
        globalrank = await codingamer.get_clash_of_code_rank()
        embed.add_field(
            name="Clash Of Code Global rank:", 
            value=f"{globalrank} ème", 
            inline=True
        )
        embed.add_field(name="Global Rank", value=f"{codingamer.rank} ème", inline=True)
        embed.add_field(name="Level:", value=str(codingamer.level), inline=False)
        embed.set_thumbnail(url=codingamer.avatar_url)
        await ctx.send(embed=embed)


    def _read_db(self):
        with open("./config/db.json", "r+") as file:
            file_data = json.load(file)
        return file_data

def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))