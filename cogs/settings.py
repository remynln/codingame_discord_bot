import json

from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor

from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        """set up your profile."""
        self.bot = bot

    @commands.command()
    async def unlink(self, ctx: commands.Context):
        """Unlink you from your actual profil."""
        loop = get_event_loop()
        file_data = await loop.run_in_executor(ThreadPoolExecutor(), self.read_db)
        if str(ctx.author.id) not in file_data.keys():
            await ctx.send("You are not linked, use !link to link your codingame profile")
            return
        if not file_data[str(ctx.author.id)]["user"]:
            await ctx.send("You are not linked, use !link to link your codingame profile")
            return
        tmp = file_data[str(ctx.author.id)]["user"]
        file_data[str(ctx.author.id)]["user"] = ""
        await loop.run_in_executor(ThreadPoolExecutor(), self.write_db, file_data)
        await ctx.send("Succesfully unlinked from " + tmp)

    @commands.command()
    async def link(self, ctx: commands.Context, arg):
        """Link you to a codingame profil."""
        loop = get_event_loop()
        file_data = await loop.run_in_executor(ThreadPoolExecutor(), self.read_db)
        if str(ctx.author.id) not in file_data.keys():
            file_data[str(ctx.author.id)] = {"user": ""}
        if file_data[str(ctx.author.id)]["user"]:
            await ctx.send("You are already linked, use !unlink to reset your link")
            return
        file_data[str(ctx.author.id)]["user"] = arg
        await loop.run_in_executor(ThreadPoolExecutor(), self.write_db, file_data)
        await ctx.send("Succesfully linked to " + arg)
    

    def read_db(self):
        with open("./config/db.json", "r+") as file:
            file_data = json.load(file)
        return file_data

    def write_db(self, file_data):
        with open("./config/db.json", "w+") as fp:
            json.dump(file_data, fp, sort_keys=True, indent=4)

def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))
