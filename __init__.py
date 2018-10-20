from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

import time
import RPi.GPIO as GPIO


# TODO read this https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins


class PicroftGoogleAiyVoicehat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(25,GPIO.OUT)
    
        self.schedule_repeating_event(self.google_aiy, None,0.5, 'GoogleAIY')

        self.add_event('recognizer_loop:record_begin',  
                    self.handle_listener_started)  
        self.add_event('recognizer_loop:record_end',  
                    self.handle_listener_ended)

    @intent_file_handler('voicehat.aiy.google.picroft.intent')
    def handle_voicehat_aiy_google_picroft(self, message):
        self.speak_dialog('voicehat.aiy.google.picroft')

    def google_aiy(self, message):
        gpio_pin=23 # The GPIO pin the button is attached to
        longpress_threshold=2 # If button is held this length of time, tells system to leave light on
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #while True:
        if GPIO.input(gpio_pin) == False: # Listen for the press, the loop until it steps
            self.log.info("Started press")
            pressed_time=time.time()
            while GPIO.input(gpio_pin) == False:
                time.sleep(0.2)
            pressed_time=time.time()-pressed_time
            self.log.info("Button pressed %d" % pressed_time)
            if pressed_time<longpress_threshold:
                # stop listning
                self.log.info("Stop listning")
                self.handle_listning()
            else:
                # start listning
                self.log.info("Start Listning")
                self.handle_listning()

    def handle_listener_started(self, message):  
        # code to excecute when active listening begins...
        self.log.info("LED ON")
        GPIO.output(25,GPIO.HIGH)

    def handle_listener_ended(self, message):  
        # code to excecute when active listening begins...  
        self.log.info("LED OFF")
        GPIO.output(25,GPIO.LOW)

    def handle_listning(self):  
        self.bus.emit(Message("rmycroft.mic.listen"))


def create_skill():
    return PicroftGoogleAiyVoicehat()

