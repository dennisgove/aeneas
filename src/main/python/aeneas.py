#!/bin/python

import logging

from flask import Flask, render_template
from flask_ask import Ask, statement

from options import Options
from controllers.mirror import MirrorController

class Aeneas(object):

  def __init__(self):
    self.options = Options()
    self.setup_logging();

    self.log.debug("Startup options: %s" % self.options.toString())

    self.setup_flask();

  def setup_logging(self):
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s %(levelname)-7s %(name)s [%(threadName)s, %(filename)s:%(lineno)d] - %(message)s'))

    self.log = logging.getLogger("aeneas")
    self.log.setLevel(self.options.logLevel())
    self.log.addHandler(console)

    flaskLogger = logging.getLogger('flask_ask')
    flaskLogger.setLevel(self.options.logLevel())
    flaskLogger.addHandler(console)

  def setup_flask(self):
    self.flaskApp = Flask(__name__)
    self.flaskApp.config["ASK_VERIFY_REQUESTS"] = False
    self.flaskAsk = Ask(self.flaskApp, '/aeneas')

    self.controllers = []
    self.controllers.append(MirrorController(self.log, self.options, self.flaskAsk))

  def start(self):
    # be aware, listening on interface 0.0.0.0 opens this up to external clients
    # if your router exposes the port then this is open to the entire world
    self.flaskApp.run(host = "0.0.0.0", port = self.options.port())

if "__main__" == __name__:
  Aeneas().start()

