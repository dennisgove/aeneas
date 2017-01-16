#!/bin/python

import urllib2
from flask_ask import statement

class MirrorController(object):

  def __init__(self, log, options, flaskAsk):
    self.log = log
    self.options = options
    self.flaskAsk = flaskAsk

    self.construct_intent_handlers()

    # Map names to mirror module ids
    # if you have the magic mirror running on port 8080 you can get the module ids using this
    # http://localhost:8080/remote?action=MODULE_DATA
    self.modules = {
      "clock" : "module_0_clock",
      "calendar" : "module_1_calendar",
      "forecast" : "module_4_weatherforecast",
      "nest" : "module_5_MMM-Nest",
      "news" : "module_6_newsfeed",
      "weather" : "module_3_currentweather",
    }

  def construct_intent_handlers(self):

    @self.flaskAsk.intent('MirrorShowHideModuleIntent',
      mapping={
        "module" : "Module",
        "action" : "Action"
      }
    )
    def show_hide_module(action, module):
      if not action in ["show", "hide"]:
        return statement("Unknown mirror action '%s'. Expecting 'show' or 'hide'" % (action))

      if "everything" == module:
        for key in self.modules:
          url = "http://localhost:8080/remote?action=%s&module=%s" % (action.upper(), self.modules[key])
          urllib2.urlopen(url).read()
        return statement("")

      elif module in self.modules:
        url = "http://localhost:8080/remote?action=%s&module=%s" % (action.upper(), self.modules[module])
        urllib2.urlopen(url).read()
        return statement("")

      else:
        return statement("Unknown module '%s'. Expecting %s, or everything" % (module, ", ".join(str(key) for key in self.modules)))

    @self.flaskAsk.intent('MirrorOnOffIntent',
      mapping={
        "state" : "State"
      }
    )
    def Module_on_off(state):
      action = { "on" : "show", "off" : "hide" }[state]
      for key in self.modules:
        url = "http://localhost:8080/remote?action=%s&module=%s" % (action.upper(), self.modules[key])
        urllib2.urlopen(url).read()
      return statement("The mirror has been turned %s" % state)
