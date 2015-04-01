__author__ = 'yanivb'

import base64

def decode_conf(value):
    """
    Decode an explosive message
    """
    if not value:
        return None

    if "@" in value:
        try:
            return "".join(chr(int(c)) for c in value.rstrip()[:-1].split("@"))

        except Exception as ex:
            print "Failed to decode value %s: %s" % ex
            return None

    return value

def encode_conf(value):
    """
    Encode an explosive message
    """
    if not value:
        return None

    try:
        return "".join(str(ord(c)) + "@" for c in value)
        return a

    except Exception as ex:
        print "Failed to encode value %s: %s" % ex
        return None

def decode_comm(value):
    if not value or not value.startswith("=="):
        raise ValueError("Message is not encoded")

    return base64.decodestring(value[::-1])[::-1]

def encode_comm(value):
    if not value:
        return None

    return base64.encodestring(value[::-1])[::-1].replace('\n','')


