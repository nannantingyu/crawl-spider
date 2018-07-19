# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import optparse
import logging
from controller import *

def parse_options():
    parser = optparse.OptionParser(
            usage=("usage: %prog [options] -c ControllerName"))
    parser.add_option("-c", "--controller", dest="controller", default="article",
            help=("controller name to run",
                  "[default %default]"))
    parser.add_option("-t", "--topic", dest="topic", default="",
                      help=("kafka topic to listen",
                            "[default %default]"))

    opts, args = parser.parse_args()
    return opts, args

if __name__ == '__main__':
    (opts, args) = parse_options()
    controllerName = "%sController" % opts.controller.capitalize()
    topic = opts.topic

    ctl = eval("%s.%s" % (controllerName, controllerName))
    if topic:
        ctl_obj = ctl(topic)
    else:
        ctl_obj = ctl()

    ctl_obj.run()