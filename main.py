from config import CONFIG_API_ID, CONFIG_API_HASH
from pyrogram import Client, filters
from cmd import Commands
import loader

bot=Client("account", api_id=CONFIG_API_ID, api_hash=CONFIG_API_HASH)
commands=Commands(".", True)


loader=loader.setup(bot,commands)
commands.add_events(bot, loader)

bot.run()
