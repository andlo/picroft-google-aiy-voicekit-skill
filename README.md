# <img src='AIY logo_blue.png' card_color='#022B4F' width='50' height='50' style='vertical-align:bottom'/> Google AIY voicekit
Enables Google AIY voicekit

## About 
This enables the led and button on the Google AIY voicekit. 

The button led turns on when Mycroft is listning. If button is pressed he begins to listen. If the button is pressed for a longer time he stops whatever he is dooing.

## Important
This skill is made for Picroft Lightning which is Picroft on Rasbian stretch and should install and initialize "out of the box". 

If you are running another installation of Mycroft and the skill isnt initialize properly, it could be that the mycroft user dont have access to the GPIO which is needed to control led and button.
You then need to add the mycroft user to the gpio group with the command 
````
sudo usermod -g gpio mycroft
````
 

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

