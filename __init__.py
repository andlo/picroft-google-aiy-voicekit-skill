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

    def __del__(self):
        self.stop()
        GPIO.cleanup(self.channel)

    def start(self):
        """Start the LED driver."""
        with self.lock:  # pylint: disable=E1129
            if not self.running:
                self.running = True
                self.pwm.start(0)  # off by default
                self.animator.start()

    def stop(self):
        """Stop the LED driver and sets the LED to off."""
        with self.lock:  # pylint: disable=E1129
            if self.running:
                self.running = False
                self.animator.join()
                self.pwm.stop()

    def set_state(self, state):
        """Set the LED driver's new state.

        Note the LED driver must be started for this to have any effect.
        """
        with self.lock:  # pylint: disable=E1129
            self.state = state

    def _animate(self):
        while True:
            state = None
            running = False
            with self.lock:  # pylint: disable=E1129
                state = self.state
                self.state = None
                running = self.running
            if not running:
                return
            if state is not None:
                if not self._parse_state(state):
                    raise ValueError('unsupported state: %d' % state)
            if self.iterator:
                self.pwm.ChangeDutyCycle(next(self.iterator))
                time.sleep(self.sleep)
            else:
                # We can also wait for a state change here with a Condition.
                time.sleep(1)

    def _parse_state(self, state):
        self.iterator = None
        self.sleep = 0.0
        handled = False

        if state == self.OFF:
            self.pwm.ChangeDutyCycle(0)
            handled = True
        elif state == self.ON:
            self.pwm.ChangeDutyCycle(100)
            handled = True
        elif state == self.BLINK:
            self.iterator = itertools.cycle([0, 100])
            self.sleep = 0.5
            handled = True
        elif state == self.BLINK_3:
            self.iterator = itertools.cycle([0, 100] * 3 + [0, 0])
            self.sleep = 0.25
            handled = True
        elif state == self.BEACON:
            self.iterator = itertools.cycle(
                itertools.chain([30] * 100, [100] * 8, range(100, 30, -5)))
            self.sleep = 0.05
            handled = True
        elif state == self.BEACON_DARK:
            self.iterator = itertools.cycle(
                itertools.chain([0] * 100, range(0, 30, 3), range(30, 0, -3)))
            self.sleep = 0.05
            handled = True
        elif state == self.DECAY:
            self.iterator = itertools.cycle(range(100, 0, -2))
            self.sleep = 0.05
            handled = True
        elif state == self.PULSE_SLOW:
            self.iterator = itertools.cycle(
                itertools.chain(range(0, 100, 2), range(100, 0, -2)))
            self.sleep = 0.1
            handled = True
        elif state == self.PULSE_QUICK:
            self.iterator = itertools.cycle(
                itertools.chain(range(0, 100, 5), range(100, 0, -5)))
            self.sleep = 0.05
            handled = True

        return handled





def create_skill():
    return PicroftGoogleAiyVoicehat()

