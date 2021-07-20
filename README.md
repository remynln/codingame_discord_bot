[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8aeedd86c1dc4ddea2b9517573c8e056)](https://www.codacy.com/gh/Waz0x/codingame_discord_bot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Waz0x/codingame_discord_bot&amp;utm_campaign=Badge_Grade)
# Discord Bot Codingame

## Install
``git clone https://github.com/Waz0x/codingame_discord_bot.git``

``pip3 install -r requirements.txt``

Go to [discord developpers portal](https://discord.com/developers/applications) create an app and setup app as bot, copy token and paste in config file.

```json
{
    "prefix": "!",
    "token": "paste here"
}
```

After that simply run the bot

``python3 main.py``

The bot is self hosted invite him with this [link](https://discord.com/api/oauth2/authorize?client_id=866601410237038592&permissions=19456&scope=bot)

## Commands

| Commands      | Actions                                                   |
| :------------:|:---------------------------------------------------------:|
| help          |   Display help message (gonna update him soon)            |
| profil        | display user profile and some stats                       |
| link          | link your codingame profile to your discord account       |
| unlink        | unlink your codingame profile to your discord account     |
| game          | send link of the actual game of clash of code             |
| next          | mention you when the next battle of clash of code start   |
| leaderboard   | :x: in a future update                                    |

## Made with

[<img src="https://avatars.githubusercontent.com/u/36101493?s=200&v=4" width="50"/>](https://discordpy.readthedocs.io/en/stable/)
[<img src="https://avatars.githubusercontent.com/u/6946974?s=200&v=4" width="50"/>](https://codingame.readthedocs.io/en/latest/)
