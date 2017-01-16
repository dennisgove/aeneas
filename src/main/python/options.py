from argparse import ArgumentParser
import logging
import json

class Options(object):

  def __init__(self):
    self.parser = ArgumentParser(description = "Alexa Skill Handler - Aeneas")

    self.parser.add_argument("-p", "--port", help="Listening port", type=int, required=True)

    self.parser.add_argument("--debug", help="Log at DEBUG level", action="store_true")
    self.parser.add_argument("--info", help="Log at INFO level", action="store_true")

    self.options = self.parser.parse_args()

  def port(self):
    return self.options.port;

  def logLevel(self):

    if(self.options.debug):
      return logging.DEBUG
    elif(self.options.info):
      return logging.INFO
    else:
      return logging.WARN

  def toString(self):
    return json.dumps(vars(self.options), separators=(", ",":"), sort_keys=True)
