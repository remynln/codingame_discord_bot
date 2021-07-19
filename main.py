import codingame
import discord
from discord.colour import Color
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
client = codingame.Client()

@bot.event
async def on_ready():
    print('Le bot est pret')

@bot.command(name="profile")
async def profile(ctx, arg):
    codingamer = client.get_codingamer(arg)
    embed = discord.Embed(title=codingamer.pseudo, url="https://www.codingame.com/profile/" + codingamer.public_handle, color=0xFF5733)
    embed.set_thumbnail(url=codingamer.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="game")
async def game(ctx):
    coc = client.get_pending_clash_of_code()
    if not coc or not coc.join_url:
        ctx.send("No games found.")
        return(84)
    embed = discord.Embed(title="Click to join", url=coc.join_url, description="**Players online:**", color=0xFF5733)
    embed.set_thumbnail(url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png")
    for player in coc.players:
        embed.add_field(name=player.pseudo, value="https://www.codingame.com/profile/" + player.public_handle)
    embed.set_footer(text="Time before start: " + str(coc.time_before_start))
    await ctx.send(embed=embed)

bot.run("/")
