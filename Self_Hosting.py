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
# This is your smartthings token
token = ''


def status(offset):
    shabbos = JewishCalendar(date.jewish_year, date.jewish_month, date.jewish_day + offset).is_assur_bemelacha()
    return shabbos


async def update_shabbos_switch(mode):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        shabbos = devices[len(devices) - 1]
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
# Remember to change back to 0,1
if (not status(0)) & status(1):
    location = GeoLocation(place, lat, long, zone, elevation=elevation)
    zmanim = ZmanimCalendar(geo_location=location, date=date.gregorian_date)
    shkia = zmanim.sunset()
    timezone = pytz.timezone(zone)
    now = datetime.now(timezone)
    time.sleep((shkia - now).total_seconds())
    main('on')
# Remember to set to 0,1
if status(0) & (not status(1)):
    location = GeoLocation(place, lat, long, zone, elevation=elevation)
    zmanim = ZmanimCalendar(geo_location=location, date=date.gregorian_date)
    havdallah = zmanim.tzais_72()
    timezone = pytz.timezone(zone)
    now = datetime.now(timezone)
    time.sleep((havdallah - now).total_seconds())
    main('off')
