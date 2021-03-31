"""Skill class to manage scheduling of meetings."""

import asyncio
import logging

from opsdroid import events
from opsdroid.skill import Skill
from opsdroid.matchers import match_event, match_regex

_LOGGER = logging.getLogger(__name__)


def html_list(sequence):
    html_items = ''.join([f"<li>{s.capitalize()}</li>" for s in sequence])
    return f"<ol>{html_items}</ol>"


class MeetingManager(Skill):
    @match_regex("!agenda$", case_sensitive=False)
    async def show_agenda(self, message):
        db = self.opsdroid.get_database("matrix")
        with db.memory_in_room(message.target):
            all_items = await self.opsdroid.memory.get("agenda_items") or []

        if all_items:
            await message.respond(html_list(all_items))
        else:
            await message.respond("There are currently no items on the agenda. Add one with `!agenda add <something we need to talk about>`")

    @match_regex("!agenda add (?P<item>.*)", case_sensitive=False)
    async def add_item(self, message):
        await message.respond(events.Message("Adding item to agenda"))

        db = self.opsdroid.get_database("matrix")

        with db.memory_in_room(message.target):
            all_items = await self.opsdroid.memory.get("agenda_items") or []

        all_items.append(message.regex.capturesdict()['item'][0])

        with db.memory_in_room(message.target):
            await self.opsdroid.memory.put("agenda_items", all_items)

    @match_regex(r"!agenda rm (?P<index>\d*)", case_sensitive=False)
    async def rm_item(self, message):
        await message.respond(events.Message("Removing item from agenda"))

        db = self.opsdroid.get_database("matrix")

        with db.memory_in_room(message.target):
            all_items = await self.opsdroid.memory.get("agenda_items") or []

        index = int(message.regex.capturesdict()['index'][0]) - 1
        try:
            all_items.remove(all_items[index])
        except IndexError:
            await message.respond("No such item. Double-check the current agenda with `!agenda`")
            return

        with db.memory_in_room(message.target):
            await self.opsdroid.memory.put("agenda_items", all_items)
