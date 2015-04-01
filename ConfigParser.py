__author__ = 'yanivb'

from pprint import pprint
import sys, os, getopt

# Are we running via IDA ?
is_ida = True
try:
    import idaapi
    import idautils
    import idc

except ImportError as err:
    is_ida = False

########################################################################
#
# Config parameters definition dictionary

param_def = {'DLD-ACT': "true/false to update default C&C servers",
            'DLD-C': "uses this value to make sure that C&C updater is valid",
            'DLD-C0': "uses this value to make sure that C&C updater is valid",
            'DLD-D': "Static C&C Updater URL",
            'DLD-E': "Dynamic C&C Updater TLD",
            'DLD-IH1': "Connection time begin",
            'DLD-IH2': "Connection time end",
            'DLD-IHC': "Take into account connection hours?",
            'DLD-IP': "Default C&C IP Address",
            'DLD-NTI': "Timing before connection attempt (seconds)",
            'DLD-P': "Dynamic C&C Updater path (relative)",
            'DLD-PRT': "Default C&C port",
            'DLD-RCH': "true/false to put value on statrup",
            'DLD-RL': "If not RCH, then uses function registerapp from DLL",
            'DLD-RN': "Current version run reg key name",
            'DLD-S': "Initial value for DGA",
            'DLD-SN': "Service name - registration related",
            'DLD-ST': "Service regiteration related",
            'DLD-TN': "Identifier transmitted upon first C&C connection",
            'DLD-USA': "related to removable device infection",
	    'DLD-USI': "USB Infection flag"}


if is_ida:
    class IdaConfigView(Choose2):
        """
        IDA GUI Menu
        """
        def __init__(self, title):
            Choose2.__init__(self, title, [ [ "Parameter", 20 | Choose2.CHCOL_PLAIN],
                                            ["Value", 50 | Choose2.CHCOL_PLAIN],
                                            ["Description", 50 | Choose2.CHCOL_PLAIN] ])
            self.n = 0
            self.icon = 41
            self.PopulateItems()

        def PopulateItems(self):
            filename = idaapi.get_input_file_path()
            with open(filename, "rb") as f:
                data = f.read()
                try:
                    settings = parse(data)
                    self.items = [ [ x, settings[x][0], settings[x][1] ] for x in settings]

                except Exception as ex:
                    print "Error while parsing configuration: %s" % ex
                    exit(1)

        def OnClose(self):
            pass

        def OnGetLine(self, n):
            return self.items[n]

        def OnGetSize(self):
            return len(self.items)

        def OnRefresh(self, n):
            self.PopulateItems()
            return n

########################################################################
#
# Get Explosive Configuration Values
#
########################################################################

def get_real_value(value):
    if "@" in value:
        return "".join(chr(int(c)) for c in value[:-1].split("@"))

    return value

def parse(data):
    settings = {}
    ignore, version, config = data.rsplit("DLD-VR", 2)
    version = version[1:-1]

    settings["DLD-VR"] = [version, "Explosive Version"]

    while len(config) > 0:
        try:
            index = config.index("DLD")
        except Exception as ex:
            break

        config = config[index:]
        param, config = config.split(':', 1)
        value, config = config.split(':' + param, 1)

        param_description = "** UNKNOWN **"
        if param in param_def:
            param_description = param_def[param]

        settings[param] = [get_real_value(value), param_description]

    return settings

########################################################################
#
# Main
#
########################################################################

if __name__ == '__main__':

    if is_ida:
        c = IdaConfigView("Explosive Config")
        c.Show()
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["input="])
        except getopt.GetoptError as err:
            print str(err)
            sys.exit(1)

        input = None
        if len(opts) < 1:
            print "not enough params"
            sys.exit(1)

        for o, a in opts:
            if o in ("-i", "--input"):
                if not os.path.isfile(a):
                    print "Could not find file %s" % a
                    sys.exit(1)

                with open(a, "rb") as f:
                    data = f.read()
                    try:
                        settings = parse(data)
                        pprint(settings)
                    except Exception as ex:
                        print "Error while parsing configuration: %s" % ex
                        exit(1)
            else:
                assert False, "unhandled option"











