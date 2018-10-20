from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

import time
import RPi.GPIO as GPIO


# TODO read this https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins


class PicroftGoogleAiyVoicehat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):

        # pin 23 is the GPIO pin the button is attached to
        # pin 25 is the GPIO pin the LED light is attached to
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(25,GPIO.OUT)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.schedule_repeating_event(self.google_aiy, None,0.1, 'GoogleAIY')

        self.add_event('recognizer_loop:record_begin',  
                    self.handle_listener_started)  
        self.add_event('recognizer_loop:record_end',  
                    self.handle_listener_ended)

    @intent_file_handler('voicehat.aiy.google.picroft.intent')
    def handle_voicehat_aiy_google_picroft(self, message):
        self.speak_dialog('voicehat.aiy.google.picroft')

    def google_aiy(self, message):
        longpress_threshold=2 
        if GPIO.input(23) == False: 
            pressed_time=time.time()
            while GPIO.input(23) == False:
                time.sleep(0.2)
            pressed_time=time.time()-pressed_time
            self.log.info("Button pressed %d" % pressed_time)
            if pressed_time<longpress_threshold:
                self.log.info("Short press")
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.log.info("Long press ")
                self.bus.emit(Message("mycroft.stop"))

    def handle_listener_started(self, message):  
        # code to excecute when active listening begins...
        self.log.info("LED ON")
        GPIO.output(25,GPIO.HIGH)

    def handle_listener_ended(self, message):  
        # code to excecute when active listening begins...  
        self.log.info("LED OFF")
        GPIO.output(25,GPIO.LOW)

def create_skill():
    return PicroftGoogleAiyVoicehat()

