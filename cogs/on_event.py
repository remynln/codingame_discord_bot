import discord
from discord.ext import commands

class OnEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        """interact with discord event."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"An error occured: {str(error)}")

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')
        activity = discord.Game(name=self.bot.config["prefix"] + "help")
        await self.bot.change_presence(activity=activity)

def setup(bot: commands.Bot):
    bot.add_cog(OnEvent(bot))
