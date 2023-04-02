# Smartthings-Shabbos-Mode
An automatic mode switcher for Shabbos and Yom Tov compatible with Smartthings Edge, self-hosted or in the cloud.


## Summary

Due to the unfortunate demise of groovy, the excellent (but sadly groovy based) [shabbat-and-holiday-modes](https://github.com/SmartThingsCommunity/SmartThingsPublic/blob/master/smartapps/shabbatholidaymode/shabbat-and-holiday-modes.src/shabbat-and-holiday-modes.groovy) will no longer function. in anticipation of this, I've created a new version that does not use groovy and should therefore be compatible with the new smartthings platform.

## Getting Started

This new solution can be a bit complicated. It can either be self-hosted on linux (and probably windows too), or, for those who don't have home servers, hosted in the cloud (AWS). I'd reccomend self-hosting, because the AWS method is much more difficult to set up, and obviously prone to service outages. Personally, I don't have a linux server, so I'm running it in AWS. It should be noted that the AWS method can still be used in free-tier. Regardless of hosting choice, the first few steps are the same. Also, if you encounter any issues, be sure to check out the accompanying [SmartThings forum](https://community.smartthings.com/t/ep-smartapp-replacement-for-shabbat-and-holiday-modes/255274), which has a lot of helpful information and troubleshooting steps.

# Setup:

### Create a virtual switch

Log into [https://graph.api.smartthings.com/device/list](https://graph.api.smartthings.com/device/list). Create a new device, and name it `Shabbos Mode Switch`. The network ID can be any random text, and make sure to set the device type to 'Simulated Switch'.

### Create an access token
Go to [https://account.smartthings.com/tokens](https://account.smartthings.com/tokens) and generate an access token. Give it any name you want, and select the devices box in 'Authorized Scopes'. Copy the generated token and store it somewhere. You'll need it for later.

# Hosting:

The next steps depend on whether you've chosen to self-host (recommended), or host on AWS. But first, download and unzip the repository.

### Self-hosting

On whatever computer you plan on hosting on, install the following dependencies:

```commandline
pip install zmanim
pip install pysmartthings
pip install aiohttp
```

Then, fill out the folllowing fields in Self_Hosting.py: 

```text
# Fill these out with your own info:
lat = 40.7128
long = -74.0060
elevation = 33
# Any name will do here
place = 'New York, NY'
# This is your timezone
zone = 'America/New_York'
# Candlelighting Offset: This is the offset of time from Shkia for the program to run
candle_lighting = -18
# Set this to True if you're in Israel
Il = False
# This is your smartthings token
token = ''
```
Note: You can find your timezone from the list on [wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) under 'TZ database name'.
Save the file, and then use `cron()` to schedule it so it runs once a day, everyday, a few minutes or so before the earliest candlelighting in your location. Skip ahead to [Finishing up](https://github.com/clippycoder/Smartthings-Shabbos-Mode/blob/main/README.md#finishing-up) to complete the process.

### Hosting in AWS
**Here is a video tutorial of the process:**


[![IAWS Setup](https://img.youtube.com/vi/-UHAucJNpWg/0.jpg)](https://www.youtube.com/watch?v=-UHAucJNpWg)


This method is a bit more involved. I won't go through it completely here, but I do in the video. In short, this is what you must do:

- Create a lambda function in python 3.9 called `Shabbos_Mode_Activator`, and for the code upload 'Shabbos_Mode_Activator.zip'. Fill in the information in the code that's marked for personalization. Then create a layer called `Dependencies` with 'Dependencies.zip'. Make sure to set 'Python 3.9' in 'compatible runtimes' option. Then add that layer to your function. Make sure to deploy the function!
- Generate root access and secret access keys for your account. They technically don't have to be root, but I have no idea what permissions they actually need, and this is my first time using lambda and boy is this stuff difficult to navigate.
- Create another lambda function called `Get_Sunset_Time` in python 3.9 and upload the code from 'Get_Sunset_Time.zip', and fill in your information + access keys in the code as well. You must also add the `Dependencies` layer. Again, make sure to deploy!
- In Amazon EventBridge, create a trigger called `Run_Shabbos_Mode` (it must be called exactly that), and schedule it with any valid `cron()` expression. It doesn't matter which expression it is, because it will be rescheduled by the program. Set it to run the lambda function `Shabbos_Mode_Activator`.
- Then create another trigger called `Get_Sunset_Activator` and schedule it with `cron()` to run the function `Get_Sunset_Time` before the earliest candlelighting of the year in your location every day. (Keep in mind that it is not DST aware!)
- As an optional but recommended step, you should test that both functions work. Run `Get_Sunset_Time` and see if it sets the time to for the `Run_Shabbos_Mode` trigger to around sunset in your local area. To test `Shabbos_Mode_Activator`,  turn on `Shabbos Mode Switch` from the app. Then set the 'TestMode' variable in the code to `True`. If it works, it will turn the switch off. Make sure to reset it to False!

# Finishing up:

You should now have a virtual switch in smartthings that will turn on at sunset before Shabbos and Yom Tov, and off 72 minutes after. To replicate the function of the old [shabbat-and-holiday-modes](https://github.com/SmartThingsCommunity/SmartThingsPublic/blob/master/smartapps/shabbatholidaymode/shabbat-and-holiday-modes.src/shabbat-and-holiday-modes.groovy), create an automation that switches your location mode to 'Shabbos' when the switch is turned on, and to whatever mode you want when the switch is turned off. And that's it! Enjoy!

---
### Notes:
- Due to the way it was designed, this system won't function in locales where sunset is after 12:00 AM. That probably won't be a problem for most people, though.
- The havdallah/tzais time is hardcoded to 72 minutes. If you want to go into the code and change it yourself, go for it.
- Beware of typos! A lot of the names here are hardcoded into the program. One misspelling could cause it to fail.
