__author__ = 'yanivb'

from pprint import pprint
import sys, os, getopt


def Genrate_DGA(initial_value):
    """
    Explosive DGA generation
    """
    domain_list = []
    domain_list.append(initial_value)
    current_domain = list(initial_value)

    while True:
        for i in xrange(0, len(current_domain)-1):
            tmp = current_domain[i+1]
            current_domain[i+1] = current_domain[i+0]
            current_domain[i] = tmp
            domain_list.append("".join(current_domain))

        if current_domain == list(initial_value):
            break

    return domain_list

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["input="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)

    input = None
    if len(opts) <1:
        print "Initial value is mandatory"
        sys.exit(1)

    for o, a in opts:
        if o in ("-i", "--input"):
            domains = Genrate_DGA(a)
            print len(domains)
            #pprint(domains)

        else:
            assert False, "Unhandled Option"
