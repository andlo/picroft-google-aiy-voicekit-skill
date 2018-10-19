from mycroft import MycroftSkill, intent_file_handler

import time
import RPi.GPIO as GPIO




class PicroftGoogleAiyVoicehat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self, channel):
        self.channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        self.pwm = GPIO.PWM(channel, 100)

    
        self.schedule_repeating_event(self.google_aiy, None,0.5, 'GoogleAIY')

        self.add_event('recognizer_loop:record_begin',  
                    self.handle_listener_started)  
        self.add_event('recognizer_loop:record_end',  
                    self.handle_listener_ended)

    @intent_file_handler('voicehat.aiy.google.picroft.intent')
    def handle_voicehat_aiy_google_picroft(self, message):
        self.speak_dialog('voicehat.aiy.google.picroft')

    def google_aiy(self, message):
        while True:
            if GPIO.input(gpio_pin) == False: # Listen for the press, the loop until it steps
                self.log.info("Started press")
                pressed_time=time.time()
                while GPIO.input(gpio_pin) == False:
                    time.sleep(0.2)
                pressed_time=time.time()-pressed_time
                self.log.info("Button pressed %d" % pressed_time)
                if pressed_time<longpress_threshold:
                    # stop listning
                    #call(['python', "/home/pi/mbus.py", "localhost", "mycroft.stop"])
                    self.pwm.ChangeDutyCycle(0)
                else:
                    # call(['python', "/home/pi/mbus.py", "localhost", "mycroft.mic.listen"])        
                    # start listning
                    self.pwm.ChangeDutyCycle(100)


    def handle_listener_started(self, message):  
        # code to excecute when active listening begins...
        self.pwm.ChangeDutyCycle(100)

    def handle_listener_ended(self, message):  
        # code to excecute when active listening begins...  
        self.pwm.ChangeDutyCycle(0)
        

def create_skill():
    return PicroftGoogleAiyVoicehat()

