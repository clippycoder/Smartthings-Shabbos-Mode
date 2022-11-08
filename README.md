# Smartthings-Shabbos-Mode
An automatic mode switcher for Shabbos and Yom Tov compatible with Smartthings Edge, self-hosted or in the cloud.


## Summary

Due to the unfortunate demise of groovy, the excellent (but sadly groovy based) [shabbat-and-holiday-modes](https://github.com/SmartThingsCommunity/SmartThingsPublic/blob/master/smartapps/shabbatholidaymode/shabbat-and-holiday-modes.src/shabbat-and-holiday-modes.groovy) will no longer function. in anticipation of this, I've created a new version that does not use groovy and should therefore be compatible with the new smartthings platform.

## Getting Started

This new solution can be a bit complicated. It can either be hosted self-hosted on linux (and probably windows too), or, for those who don't have home-servers, hosted in the cloud (AWS). self-hosting is recommended, because the AWS method is much more difficult to set up. It should be noted that the AWS method can still be used in free-tier. Regardless of hosting choice, the first few steps are the same.

# Setup:

### Create a virtual switch

Log into [https://graph.api.smartthings.com/device/list](https://graph.api.smartthings.com/device/list). Create a new device, and name it 'Shabbos Mode Switch'. The newtwork ID can be any random text, and make sure to set the device type to 'Simulated Switch'.

### Create an access token
Go to [https://account.smartthings.com/tokens](https://account.smartthings.com/tokens) and generate an access token. Give it any name you want, and select the devices box in 'Authorized Scopes'. Copy the generated token and store it somewhere. You'll need it for later.

### Find the virtual switch's device number

download the .zip file and install the following dependencies:
```commandline
pip install zmanim
pip install pysmartthings
pip install aiohttp
```

Then edit 'get-shabbos-switch-number.py', and enter your  access token in the field marked `token = ''`.

Run the program, and scan the output to find 'Shabbos Mode Switch'. Note the number next to it; that's the device number.

# Hosting:

The next steps depend on wether you've chosen to self-host (recommended), or host on AWS.

### Self-hosting

On whatever computer you plan on hosting on, make sure you have the same dependencies as before installed. Then, fill out the folllowing fields in auto-shabbos-mode-self-hosted.py:
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
# This is your device number,it can be found by using
# the get-shabbos-switch-number.py program.
devicenum = 39
```
Save the file, and then use `cron()` to schedule it so it runs everyday before sunset. Skip ahead to finallization to complete the process.

### Hosting in AWS

This is method is a bit more involved. I won't go through it completely, but in short, this is what you must do:

- Create a lambda function in python 3.9 called 'Shabbos_Mode_Activator', and for the code upload 'Shabbos_Mode_Activator.zip'. Fill in the information in the code that needs personalization. Then create create and add a layer called 'Dependencies' with 'Dependencies.zip'.
- Generate root access and secret access keys for your account. They technically. don't have to be root, but I have no idea what permissions they actually need.
- Create another lambda function called 'Get_Sunset_Time' in python 3.9 and fill in your information + access keys as well and upload the code from 'Get_Sunset_Time.zip'. You must add the 'Dependencies' layer as well.
- In Amazon EventBridge, create a trigger called 'Run_Shabbos_Mode' (it must be called exactly that), and schedule it with any valid `cron()` expression.
- Then create another trigger called 'Get_Sunset_Activator' and schedule it with `cron()` to run before the earliest sunset of the year every day. That shoulf be all.

# Finalization:

You should now have a virtual switch in smartthings that will turn on at sunset before Shabbos and Yom Tov, and off 72 minutes after. To replicate the function of the old [shabbat-and-holiday-modes](https://github.com/SmartThingsCommunity/SmartThingsPublic/blob/master/smartapps/shabbatholidaymode/shabbat-and-holiday-modes.src/shabbat-and-holiday-modes.groovy), create an automation that switches your location mode to 'Shabbos' when the switch is turned on, and to whatever mode you want when the switch is turned off. And that's it! Enjoy!

---
### Notes:
- Due to the way it was designed, this system won't function in locales where sunset is after 12:00 AM. That probably won't be a problem for most people though.
- The havdallah/tzais time is set to 72 minutes. If you want to go into the code and change it yourself, go for it.
