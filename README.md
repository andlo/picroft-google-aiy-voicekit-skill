# <img src='AIY_logo_blue.png' card_color='#022B4F' width='50' height='50' style='vertical-align:bottom'/> Google AIY voicekit
Enables Google AIY voicekit

## About
This enables the led and button on the Google AIY voicekit.

The button led turns on when Mycroft is listning. If button is pressed he begins to listen. If the button is pressed for a longer time he stops whatever he is dooing.

## Important
This skill is made for Picroft Lightning which is Picroft on Rasbian stretch and should install and initialize "out of the box".

If you are running another installation of Mycroft and the skill isnt initialize properly, it could be that the mycroft user dont have access to the GPIO which is needed to control led and button.
You then need to add the mycroft user to the gpio group with the command
```
sudo usermod -g gpio mycroft
```
### Installing the AIY voicekit
If you hassnt alreddy setup the voicekit, there is a script to help you do that in the skills folder.

run
```
install_AIY.sh
```
This script will add google's AIY reposotories, update and install the nessesary drivers and reconfigure the Pi to enable the kit.
You need to do a reboot afterwords.

## Category
**IoT**

## Credits
Andreas Lorensen (@andlo)

## Supported Devices
platform_picroft

## Tags
#googlevoicekit
#aiy
#Googleaiy
#voicekit
#voicehat

