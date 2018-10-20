from mycroft import MycroftSkill, intent_file_handler

import time
import RPi.GPIO as GPIO




class PicroftGoogleAiyVoicehat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        my_led = LED(channel = 25)
        my_led.start()
        my_led.set_state(LED.PULSE_QUICK)
        
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(channel, GPIO.OUT)
        #self.pwm = GPIO.PWM(self.channel, 100)

        

    
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
                    #self.pwm.ChangeDutyCycle(0)
                    self.log.info("Longpress button")
                else:
                    # call(['python', "/home/pi/mbus.py", "localhost", "mycroft.mic.listen"])        
                    # start listning
                    #self.pwm.ChangeDutyCycle(100)
                    self.log.info("press button")


    def handle_listener_started(self, message):  
        # code to excecute when active listening begins...
        #self.pwm.ChangeDutyCycle(100)
        my_led.set_state(LED.ON)

    def handle_listener_ended(self, message):  
        # code to excecute when active listening begins...  
        #self.pwm.ChangeDutyCycle(0)
        my_led.set_state(LED.OFF)

class LED:
    """
    Simple usage:
        my_led = LED(channel = 25)
        my_led.start()
        my_led.set_state(LED.BEACON)
        my_led.stop()
    """

    OFF = 0
    ON = 1
    BLINK = 2
    BLINK_3 = 3
    BEACON = 4
    BEACON_DARK = 5
    DECAY = 6
    PULSE_SLOW = 7
    PULSE_QUICK = 8

    def __init__(self, channel):
            self.animator = threading.Thread(target=self._animate)
            self.channel = channel
            self.iterator = None
            self.running = False
            self.state = None
            self.sleep = 0
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(channel, GPIO.OUT)
            self.pwm = GPIO.PWM(channel, 100)
            self.lock = threading.Lock()

    



def create_skill():
    return PicroftGoogleAiyVoicehat()

