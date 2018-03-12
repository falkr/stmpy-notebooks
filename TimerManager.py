import paho.mqtt.client as mqtt
from stmpy import Driver, Machine
from threading import Thread

BROKER = 'test.mosquitto.org'
PORT = 1883


class TimerLogic:
    """
    This is th esupport object for a state machine that models a single
    timer.
    """
    def __init__(self, name):
        self.name = name

    def started(self):
        print('Timer started!')


class TimerManager:
    """
    The ecomponent to manage named timers.
    """
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {}".format(rc))

    def on_message(self, client, userdata, msg):
        print("Message received with topic {}".format(msg.topic))
        print("{}".format(msg.payload))
        print('--------')

        # TODO: Here you will porbably add a lot of code!

        # let's create a state machine, just as an example
        new_timer_name = 'spaghetti'
        timer_logic = TimerLogic(name=new_timer_name)
        t0 = {'source': 'initial',
              'target': 'active',
              'effect': 'started'}
        timer_stm = Machine(name=new_timer_name, transitions=[t0], obj=timer_logic)
        self.driver.add_machine(timer_stm)




    def __init__(self):
        # create a new client and set the callback methods
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.connect(BROKER, PORT)
        # subscribe to proper topic(s) of your choice
        self.client.subscribe("ttm415/teamx")

        # we start the stmpy driver
        self.driver = Driver()
        self.driver.start(keep_active=True)

        thread = Thread(target=self.client.loop_forever())
        thread.start()


t = TimerManager()
