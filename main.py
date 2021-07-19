import asyncio
from asyncio.tasks import wait
import codingame
import discord
import random
import json
from discord.colour import Color
from discord.ext import commands

with open("./config/config.json", "r") as cjson:
    config = json.load(cjson)
bot = commands.Bot(command_prefix=config["prefix"])
client = codingame.Client()

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")

@bot.event
async def on_ready():
    print('Le bot est pret')
    presences = ["!game to join a game", "!profile to get a profile", "coding ..."]
    while not bot.is_closed:
        presence = random.choice(presences)
        await bot.change_presence(activity=discord.Game(name=presence))
        await asyncio.sleep(6)

@bot.command(name="profil")
async def profil(ctx, arg):
    codingamer = client.get_codingamer(arg)
    embed = discord.Embed(title=codingamer.pseudo, url="https://www.codingame.com/profile/" + codingamer.public_handle, color=Color.orange())
    embed.add_field(name="Clash Of Code Global rank:", value=str(codingamer.get_clash_of_code_rank()) + " ème", inline=True)
    embed.add_field(name="Global Rank", value=str(codingamer.rank) + " ème", inline=True)
    embed.add_field(name="Level:", value=str(codingamer.level), inline=False)
    embed.set_thumbnail(url=codingamer.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="game")
async def game(ctx):
    coc = client.get_pending_clash_of_code()
    embed = discord.Embed(title="Click to join", url=coc.join_url, description="**Players online:**", color=Color.blue())
    embed.set_thumbnail(url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png")
    for player in coc.players:
        embed.add_field(name=player.pseudo, value="[See profil](https://www.codingame.com/profile/" + player.public_handle + ")")
    embed.set_footer(text="Time before start: " + str(coc.time_before_start.seconds) + "s")
    await ctx.send(embed=embed)

@bot.command(name="next")
async def next(ctx):
    coc = client.get_pending_clash_of_code()
    next_battle = coc.time_before_start.seconds
    await ctx.send("Next battle in " + str(next_battle) + "s ~")
    while next_battle > 5:
        coc = client.get_pending_clash_of_code()
        next_battle = coc.time_before_start.seconds
        print(next_battle)
        await asyncio.sleep(5)
    await asyncio.sleep(next_battle + 5)
    await ctx.send(ctx.author.mention)
    coc = client.get_pending_clash_of_code()
    while not coc:
        coc = client.get_pending_clash_of_code()
        asyncio.sleep(1)
    embed = discord.Embed(title="Click to join", url=coc.join_url, description="**Players online:**", color=Color.blue())
    embed.set_thumbnail(url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png")
    for player in coc.players:
        embed.add_field(name=player.pseudo, value="https://www.codingame.com/profile/" + player.public_handle)
    embed.set_footer(text="Time before start: " + str(coc.time_before_start))
    await ctx.send(embed=embed)

bot.run(config["token"])