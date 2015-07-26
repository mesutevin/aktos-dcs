try:
    import simplejson as json
except ImportError:
    print "WARNING: module simplejson not found, using json insead..."
    import json

import time
import uuid

# message functions
def message_decoder(json_string):
    try:
        j = json.loads(json_string)
        c = globals()[j["cls"]]
        del(j["cls"])
        o = c(**j)
    except Exception as e:
        reason = "(other reasons)"
        try:
            assert not pack(json_string)
        except AssertionError:
            reason = "message is not JSON string, pack first."
        raise Exception("Error unpacking message: %s" % reason)

    return o

def unpack(json_string):
    return message_decoder(json_string)

def pack(msg):
    assert(isinstance(msg, Message))
    msg.cls = msg.__class__.__name__
    #return json.dumps(msg, cls=MessageEncoder)
    return json.dumps(dict(msg))

class Message(dict):
    """
    msg_id = ""  # unique id of message
    timestamp = time.time()
    msg_id = str(uuid.uuid4())
    sender = []
    debug = []
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

        """
        try:
            for attr in dir(self):
                if not callable(getattr(self, attr)) and not attr.startswith("__"):
                    #print attr
                    default_val = getattr(self, attr)
                    delattr(Message, attr)
                    setattr(self, attr, default_val)
        except:
            import pdb
            pdb.set_trace()

        """
        self.msg_id = ""  # unique id of message
        self.timestamp = time.time()
        self.msg_id = str(uuid.uuid4())
        self.sender = []
        self.debug = []
        self.cls = self.__class__.__name__

        # this should be the last one
        for k, v in kwargs.items():
            setattr(self, k, v)


class ProxyActorMessage(Message):
    contact_list = dict()
    new_contact_list = dict()
    reply_to = ""



# TODO: Classes defined below are belong to application. Move them!

class KeypadMessage(Message):
    edge = None
    key = ""

class IoMessage(Message):
    edge = ""
    pin_name = ""
    pin_number = 0
    curr_val = 0
    prev_val = 0
    last_change = -1
    def __init__(self, **kwargs):
        try:
            self.pin_name = kwargs["sender"].pin_name
        except:
            pass

        try:
            self.pin_number = kwargs["sender"].pin_number
        except:
            pass

        Message.__init__(self, **kwargs)

class GetIoStatusMessage(IoMessage):
    pass

class IoStatusMessage(GetIoStatusMessage):
    pass

class RedLightMessage(Message):
    mode = ""

class UserInputMessage(Message):
    screen_str = ""
    msg_id = 0

    def get_msg_group(self):
        # get the first digit as string

        group_num = str(self.msg_id)[0]
        return int(group_num)


class ScreenMessage(Message):
    screen_str = ""


class AlarmMessage(Message):
    reason = ""


class AlarmResetMessage(AlarmMessage):
    pass


class AlarmGenJumpToState(Message):
    state = 0


class PingMessage(Message):
    text = ""


class PongMessage(PingMessage):
    pass


class aMessage(Message):
    direction = ""  # up, down, none


def test():
    a = Message(key="d", edge="rising_edge")
    a.sender.append("naber")

    b = KeypadMessage()
    b.sender.append("iyidir")

    assert len(str(a)) == len(pack(a))
    assert a == unpack(pack(a))
    assert len(str(b)) == len(pack(b))
    assert b == unpack(pack(b))
    print "all tests OK..."

if __name__ == "__main__":
    try:
        test()
    except:
        raise

        import pdb
        pdb.set_trace()



