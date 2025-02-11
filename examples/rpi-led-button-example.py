import add_import_path # only for examples

from aktos_dcs import *
from aktos_dcs_lib import *

class Test(Actor):
    def handle_IoMessage(self, msg):
        msg_body = get_msg_body(msg)

        print("Got message: %s", msg_body["val"])

    def action(self):
        val = False
        while True:
            sleep(2)
            print("sending value: %s" % val)
            self.send({'IoMessage': {'pin_name': 'test-output-1', 'val': val}})
            val = not val

if __name__ == "__main__":
    output_pins = {
        'test-output-1': 2,
    }
    input_pins = {
        'test-input-1': 3,
    }

    for k, v in input_pins.items():
        GPIOInputActor(pin_name=k, pin_number=v, invert=True)

    for k, v in output_pins.items():
        GPIOOutputActor(pin_name=k, pin_number=v, initial=True)

    Test()

    try:
        wait_all()
    except:
        print "CLEANIN UP!"
        import RPi.GPIO as g
        g.cleanup()
