__author__ = 'ceremcem'

from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs.Messages import *


class Ponger(Actor):
    def handle_PongMessage(self, msg):
        print "Ponger got pong message:", msg.text, (time.time() - msg.timestamp), msg.debug
        sleep(1)
        self.send(PingMessage(text="Hello pinger, this is ponger cca!"))

if __name__ == "__main__":
    ProxyActor(brokers="192.168.2.119:5012:5013")
    ponger = Ponger()
    ponger.send(PingMessage(text="startup message from ponger 1..."))

    ponger.join()
