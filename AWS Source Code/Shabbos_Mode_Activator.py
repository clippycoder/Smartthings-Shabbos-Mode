from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
import time
import pysmartthings
import aiohttp
import asyncio
import json
import os

# This is your smartthings token
token = ''
# Enter your own timezone here:
os.environ['TZ'] = 'America/New_York'
# Set to True if you're in Israel
Il = False
# Set to True to test the function
TestMode = False


def status(offset):
    test = date + offset
    shabbos = JewishCalendar(test.jewish_year, test.jewish_month, test.jewish_day, in_israel=Il).is_assur_bemelacha()
    return shabbos


async def update_shabbos_switch(mode):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        i = 0
        while devices[i].name.lower() != 'shabbos mode switch':
            i += 1
        shabbos = devices[i]
        if mode == 'off':
            await shabbos.switch_off()
        else:
            await shabbos.switch_on()


def main(mode):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(update_shabbos_switch(mode))
    loop.close()


time.tzset()
date = JewishDate()


def lambda_handler(event, context):
    if (not status(0)) & status(1) and not TestMode:
        main('on')
    if status(0) & (not status(1)) or TestMode:
        main('off')
    return {
        'statusCode': 200,
        'body': json.dumps('function has been run')
    }
