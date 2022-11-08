# Smartthings-Shabbos-Mode
An automatic mode switcher for Shabbos and Yom Tov compatible with Smartthings Edge, self-hosted or in the cloud.


## Summary

Due to the unfortunate demise of groovy, the excellent (but sadly groovy based) [shabbat-and-holiday-modes](https://github.com/SmartThingsCommunity/SmartThingsPublic/blob/master/smartapps/shabbatholidaymode/shabbat-and-holiday-modes.src/shabbat-and-holiday-modes.groovy) will no longer function. in anticipation of this, I've created a new version that does not use groovy and should therefore be compatible with the new smartthings platform.

## Getting Started

This new solution can be a bit complicated. It can either be self-hosted on linux (and probably windows too), or, for those who don't have home servers, hosted in the cloud (AWS). I'd reccomend self-hosting, because the AWS method is much more difficult to set up, and obviously prone to service outages. Personally, I don't have a linux server, so I'm running it in AWS. It should be noted that the AWS method can still be used in free-tier. Regardless of hosting choice, the first few steps are the same.

# Setup:

### Create a virtual switch

Log into [https://graph.api.smartthings.com/device/list](https://graph.api.smartthings.com/device/list). Create a new device, and name it 'Shabbos Mode Switch'. The network ID can be any random text, and make sure to set the device type to 'Simulated Switch'.

### Create an access token
Go to [https://account.smartthings.com/tokens](https://account.smartthings.com/tokens) and generate an access token. Give it any name you want, and select the devices box in 'Authorized Scopes'. Copy the generated token and store it somewhere. You'll need it for later.

# Hosting:

The next steps depend on wether you've chosen to self-host (recommended), or host on AWS.

### Self-hosting

On whatever computer you plan on hosting on, install the following dependencies:

```commandline
pip install zmanim
pip install pysmartthings
pip install aiohttp
```

Then, fill out the folllowing fields in auto-shabbos-mode-self-hosted.py:

```text
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
```

Save the file, and then use `cron()` to schedule it so it runs everyday before sunset. Skip ahead to Finishing up to complete the process.

### Hosting in AWS

This is method is a bit more involved. I won't go through it completely, but in short, this is what you must do:

- Create a lambda function in python 3.9 called 'Shabbos_Mode_Activator', and for the code upload 'Shabbos_Mode_Activator.zip'. Fill in the information in the code that's marked for personalization. Then create and add a layer called 'Dependencies' with 'Dependencies.zip'.
- Generate root access and secret access keys for your account. They technically don't have to be root, but I have no idea what permissions they actually need, and this is my first time using lambda and boy is this stuff difficult to navigate.
- Create another lambda function called 'Get_Sunset_Time' in python 3.9 and upload the code from 'Get_Sunset_Time.zip', and fill in your information + access keys in the code as well. You must also add the 'Dependencies' layer.
- In Amazon EventBridge, create a trigger called 'Run_Shabbos_Mode' (it must be called exactly that), and schedule it with any valid `cron()` expression. Set it to run the lambda function 'Shabbos_Mode_Activator'.
- Then create another trigger called 'Get_Sunset_Activator' and schedule it with `cron()` to run the function 'Get_Sunset_Time' before the earliest sunset of the year in your location every day. (Keep in mind that it is not DST aware!)

# Finishing up:

You should now have a virtual switch in smartthings that will turn on at sunset before Shabbos and Yom Tov, and off 72 minutes after. To replicate the function of the old [shabbat-and-holiday-modes](https://github.com/SmartThingsCommunity/SmartThingsPublic/blob/master/smartapps/shabbatholidaymode/shabbat-and-holiday-modes.src/shabbat-and-holiday-modes.groovy), create an automation that switches your location mode to 'Shabbos' when the switch is turned on, and to whatever mode you want when the switch is turned off. And that's it! Enjoy!

---
### Notes:
- Due to the way it was designed, this system won't function in locales where sunset is after 12:00 AM. That probably won't be a problem for most people, though.
- The havdallah/tzais time is hardcoded to 72 minutes. If you want to go into the code and change it yourself, go for it.
- The program cannot currently differentiate between more than one virtual switch. Unfortunately, this means only one virtual switch per account is supported.
