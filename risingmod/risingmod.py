import datetime
import json
import logging
import sys
import traceback
import discord

from discord.ext import commands
from collections import Counter, deque
from risingmod.config import *

description = """
Discord bot focused on moderation and user engagement, originally created for Rising Hub's discord server.
"""

log = logging.getLogger(__name__)

extensions = (
    'extensions.about'
)


def _resolve_prefix(bot, msg):
    uid = bot.user.id
    valid = [f'<@!{uid}> ', f'<@{uid}> ', bot_prefix]
    return valid


class RisingMod(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_resolve_prefix, description=description,
                         pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)

        self.uptime = None
        self._prev_events = deque(maxlen=10)

        self.spam_control = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)
        self._auto_spam_count = Counter()

        for extension in extensions:
            try:
                self.load_extension(f'risingmod.{extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_socket_response(self, msg):
        self._prev_events.append(msg)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def on_resumed(self):
        print('resumed.')

    async def shutdown(self):
        await super().close()
        await self.session.close()

    def run(self):
        try:
            super().run(bot_token, reconnect=True)
        finally:
            with open('risingmod_prev_events.log', 'w', encoding='utf-8') as fp:
                for data in self._prev_events:
                    try:
                        x = json.dumps(data, ensure_ascii=True, indent=4)
                    except:
                        fp.write(f'{data}\n')
                    else:
                        fp.write(f'{x}\n')
