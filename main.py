import asyncio
import codingame
import discord
from discord.colour import Color
from discord.ext import commands
import config
from db import db

bot = commands.Bot(command_prefix=config.prefix,
                   activity=discord.Game(name=config.activity_status))
client = codingame.Client(is_async=True)


@bot.event
async def on_command_error(ctx, error):
    if config.debug:
        await ctx.send(f"An error occurred: {str(error)}")
    raise error


@bot.event
async def on_ready():
    print("Bot is ready to go")
    print("-" * 10)

# Unregister a user's codingame profile when the unlink command is used
# It uses the databases connection to check if the user is linked to a profile
# If not, it unlinks the user from the database
@bot.command()
async def unlink(ctx):
    user = ctx.message.author
    if not db.is_linked(user.id):
        await ctx.send("You are not linked to a codingame profile")
        return
    db.unlink(user.id)
    await ctx.send(f"{user.mention}'s codingame profile has been unlinked")


# Register a user's codingame profile when the link command is used
# It uses the databases connection to check if the user is linked to a profile
# If not, it links the user to the database
@bot.command()
async def link(ctx, arg):
    user = ctx.message.author
    if db.is_linked(user.id):
        await ctx.send("You are already linked to a codingame profile")
        return
    db.link(user.id, arg)
    await ctx.send(f"{user.mention}'s codingame profile has been linked")


# Get a codingame profile when the profile command is used
# If there is an argument, it gets the user's profile id from the argument
# Else it gets the user's profile id from the database
@bot.command()
async def profile(ctx, arg=None):
    user = ctx.message.author
    profile_id = arg
    if arg is None:
        if not db.is_linked(user.id):
            await ctx.send("You are not linked to a codingame profile")
            return
        profile_id = db.get_codingame_id(user.id)
    codingamer = await client.get_codingamer(profile_id)
    # TODO: Make this work cause damn idk why it's not
    if codingamer is None:
        await ctx.send(f"There is no profile with id {profile_id}")
        return
    await ctx.send(
        embed=discord.Embed(title=codingamer.pseudo,
                            url="https://www.codingame.com/profile/" + codingamer.public_handle,
                            color=Color.orange())
            .add_field(name="Clash Of Code Global rank:",
                       value=str(await codingamer.get_clash_of_code_rank()) + " ème",
                       inline=True)
            .add_field(name="Global Rank",
                       value=str(codingamer.rank) + " ème",
                       inline=True)
            .add_field(name="Level:",
                       value=str(codingamer.level),
                       inline=False)
            .set_thumbnail(url=codingamer.avatar_url)
    )


@bot.command(name="info", description="Display info about the bot")
async def info(ctx):
    await ctx.send(
        embed=discord.Embed(title="Infos", color=Color.gold())
            .add_field(name="Invite me",
                       value="[here](" + config.invitation_link + ")")
            .add_field(name="Source Code", value="[here](" + config.source_code_link + ")")
            .set_thumbnail(url=config.codingame_icon_link)
            .set_footer(text="Made with <3 by Waz0x and huntears")
    )


bot.run(config.token)
