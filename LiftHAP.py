# An Accessory for a LED attached to pin 11.
import logging

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_GARAGE_DOOR_OPENER, CATEGORY_WINDOW_COVERING, CATEGORY_WINDOW

FIFO = "/var/run/gpio.fifo"

class Lift(Accessory):

    #category = CATEGORY_GARAGE_DOOR_OPENER
    category = CATEGORY_WINDOW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #serv_light = self.add_preload_service('GarageDoorOpener')
        serv_light = self.add_preload_service('Window')
        self.char_state = serv_light.configure_char(
            'TargetPosition', setter_callback=self.operate_lift)

    '''
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._gpio_setup(self.pin)
    '''

    def operate_lift(self, value):
        print(value)
        if value == "Open" or value > 50:
            cmd = "u"
        elif value == "Closed" or value <= 50:
            cmd = "d"
        else:
            return
        with open(FIFO, "w") as fifo:
            fifo.write(cmd + "\n")

    def stop(self):
        super().stop()
