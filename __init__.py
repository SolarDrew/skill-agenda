"""Skill class to manage scheduling of meetings."""

import asyncio
import logging

from opsdroid import events
from opsdroid.skill import Skill
from opsdroid.matchers import match_event, match_regex

_LOGGER = logging.getLogger(__name__)


class MeetingManager(Skill):
    @match_event(events.Message)
    async def on_message(self, message):
        _LOGGER.debug("Received a Message event from the connector")
        await message.respond(events.Message("I don't take orders from you."))

    @match_event(cdevents.UpcomingEvent)
    async def send_chat_reminder(self, upcoming):
        _LOGGER.debug("Reminder event detected, forwarding to chat.")
        # get new target - default to loading from config
        # mconn = get_matrix_connector()
        # target_room = mconn.rooms[self.config.get("reminder-room", "main")]
        # # construct message from reminder info
        # reminder = events.Message(
        #     f"You've got a meeting coming up! {upcoming.name} is coming up at {upcoming.start_time} and is scheduled to continue until {upcoming.end_time}.", target=target_room
        # )
        # send message
        print(f"Remember about {upcoming.name} at {upcoming.start_time} until {upcoming.end_time}.")
