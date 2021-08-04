import os
import json
import codingame

import discord
from discord.ext import commands

with open("./config/config.json", "r") as cjson:
    config = json.load(cjson)
with open("./config/db.json", "r") as dbjson:
    db = json.load(dbjson)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

bot.config = config
bot.codingame_client = codingame.Client(is_async=True)

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(config["token"])