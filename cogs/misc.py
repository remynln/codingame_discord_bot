import discord
from discord.colour import Color
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        """Some other commands."""
        self.bot = bot

    @commands.command()
    async def info(self, ctx: commands.Context):
        """Display info on the bot."""
        embed = discord.Embed(title="Infos", color=Color.gold())
        embed.add_field(
            name="Invite me",
            value="[here](https://discord.com/api/oauth2/authorize?client_id=866601410237038592&permissions=8&scope=bot)"
        )
        embed.add_field(name="Source Code", value="[here](https://github.com/Waz0x/codingame_discord_bot)")
        embed.set_thumbnail(
            url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png"
        )
        embed.set_footer(
            text="Made with <3 by Waz0x",
            icon_url="https://cdn.discordapp.com/avatars/606758395583922176/0ab96a13c0e7998926b1ffdfa9364313.png?size=128"
        )
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))