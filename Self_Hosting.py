from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.util.geo_location import GeoLocation
import pytz
from datetime import datetime
import time
import pysmartthings
import aiohttp
import asyncio
import os

# Fill these out with your own info:
lat = 40.7128
long = -74.0060
elevation = 33
# Any name will do here
place = 'New York, NY'
# This is your timezone
zone = 'America/New_York'
# Set this to True if you're in Israel
Il = False
# This is your smartthings token
token = '2adfd1a0-bbe4-4048-b86c-4818dfb28674'


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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_shabbos_switch(mode))
    loop.close()


date = JewishDate()
os.environ['TZ'] = zone

if (not status(0)) & status(1):
    location = GeoLocation(place, lat, long, zone, elevation=elevation)
    zmanim = ZmanimCalendar(geo_location=location, date=date.gregorian_date)
    shkia = zmanim.sunset()
    timezone = pytz.timezone(zone)
    now = datetime.now(timezone)
    time.sleep((shkia - now).total_seconds())
    main('on')

if status(0) & (not status(1)):
    location = GeoLocation(place, lat, long, zone, elevation=elevation)
    zmanim = ZmanimCalendar(geo_location=location, date=date.gregorian_date)
    havdallah = zmanim.tzais_72()
    timezone = pytz.timezone(zone)
    now = datetime.now(timezone)
    time.sleep((havdallah - now).total_seconds())
    main('off')
