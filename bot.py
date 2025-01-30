
import sys
import glob
import importlib
from pathlib import Path
from pyrogram import idle
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz
from aiohttp import web
from plugins import web_server, check_expired_premium

import asyncio
from pyrogram import idle
from lazybot import LazyPrincessBot
from util.keepalive import ping_server
from lazybot.clients import initialize_clients





async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL_1:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_1)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_1)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_1)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL_1 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL_1}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/TitanMattersSupport for support")
                sys.exit()
        if FORCE_SUB_CHANNEL_2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL_2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL_2}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/TitanMattersSupport for support")
                sys.exit()
        if FORCE_SUB_CHANNEL_3:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_3)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_3)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_3)).invite_link
                self.invitelink3 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL_3 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL_3}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/TitanMattersSupport for support")
                sys.exit()
        if FORCE_SUB_CHANNEL_4:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_4)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_4)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_4)).invite_link
                self.invitelink4 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL_4 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL_4}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/TitanMattersSupport for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/TitanMattersSupport for support")
            sys.exit()

        







ppath = "plugins/*.py"
files = glob.glob(ppath)
LazyPrincessBot.start()
loop = asyncio.get_event_loop()


async def Lazy_start():
    print('\n')
    print('Initalizing Deendayal Dhakad Bot')
    bot_info = await LazyPrincessBot.get_me()
    LazyPrincessBot.username = bot_info.username
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Deendayal dhakad Imported => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    await Media.ensure_indexes()
    me = await LazyPrincessBot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    LazyPrincessBot.username = '@' + me.username
    LazyPrincessBot.loop.create_task(check_expired_premium(LazyPrincessBot))
    logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    logging.info(LOG_STR)
    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    await LazyPrincessBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()                     

if __name__ == '__main__':
    try:
        loop.run_until_complete(Lazy_start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
