import json
import boto3
from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.util.geo_location import GeoLocation
from datetime import datetime
from zoneinfo import ZoneInfo

# Fill these out with your own info:
lat = 40.632
long = -73.7126
elevation = 23
zone = 'America/New_York'
# I don't think this one makes a difference
place = 'New York, NY'
# Set this to True if you're in Israel
Il = False
# Enter your server location and keys here:
REGION_NAME = 'us-east-1'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''


def status(offset):
    test = date + offset
    shabbos = JewishCalendar(test.jewish_year, test.jewish_month, test.jewish_day, in_israel=Il).is_assur_bemelacha()
    return shabbos


client = boto3.client('events',
                      region_name=REGION_NAME,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


date = JewishDate()


def lambda_handler(event, context):
    location = GeoLocation(place, lat, long, zone, elevation=elevation)
    zmanim = ZmanimCalendar(geo_location=location, date=datetime.now())
    if not status(0):
        shkia = zmanim.sunset().astimezone(ZoneInfo('UTC'))
        hours = shkia.strftime('%H')
        minutes = shkia.strftime('%M')
        client.put_rule(Name='Run_Shabbos_Mode', ScheduleExpression='cron(' + minutes + ' ' + hours + ' * * ? *)')
    else:
        havdallah = zmanim.tzais_72().astimezone(ZoneInfo('UTC'))
        hours = havdallah.strftime('%H')
        minutes = havdallah.strftime('%M')
        client.put_rule(Name='Run_Shabbos_Mode', ScheduleExpression='cron(' + minutes + ' ' + hours + ' * * ? *)')
    return {
        'statusCode': 200,
        'body': json.dumps('Set sunset trigger time')
    }
