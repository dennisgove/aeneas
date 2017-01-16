#!/bin/python

from flask_ask import statement
from hue_api import HueApi

class HueController(object):

  def __init__(self, log, options, flaskAsk):
    self.log = log
    self.options = options
    self.flaskAsk = flaskAsk

    self.construct_intent_handlers()
    self.api = HueApi(self.log)
    switches = self.api.get_visible_switches()
    print switches
    print self.api.register_client(switches[0]["ip"])

  def construct_intent_handlers(self):

    @self.flaskAsk.intent('HueOnOffIntent',  
      mapping={
        "room" : "Room",
        "device" : "Device",
        "state" :"State"
      }
    )
    def hue_on_off(room, device, state):
      text = "Hi, turning '%s' '%s' '%s'" % (room, device, state)
      return statement(text)

    @self.flaskAsk.intent('HueDeviceDetailIntent',  
      mapping={
        "room" : "Room"
      }
    )
    def hue_device_detail(room):
      text = "Hi, '%s' has some devices" % (room)
      return statement(text)

