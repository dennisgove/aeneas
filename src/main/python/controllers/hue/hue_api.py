#!/bin/python

import json
import os.path
import requests

class HueApi(object):

  def __init__(self, log):
    self.log = log

  def get_visible_switches(self):
    url = "https://www.meethue.com/api/nupnp"
    try:
      return [{
        "id" : str(rec["id"]), 
        "ip" : str(rec["internalipaddress"]),
        "name" : self.get_switch_name(rec["internalipaddress"])
      } for rec in requests.get(url).json()]

    except Exception as e:
      self.log.error("Failed to get Hue Switch info from %s with error '%s'" % (url, e))
      return None

  def get_switch_name(self, ip):
    try:
      return str(requests.get("http://%s/api/config" % ip).json()["name"])

    except Exception as e:
      self.log.error("Failed to get Hue Switch name from %s with error '%s'" % (ip, e))
      return None

  def register_switch_client(self, ip):
    try:
      response = requests.post("http://%s/api" % ip, data = json.dumps({"devicetype":"aeneas#hue"})).json()[0]
      print response
      if "error" in response:
        self.log.info("User didn't press the button on switch %s" % ip)
        return None
      elif "success" in response:
        return (True, "")
        return response["success"]["username"]

    except Exception as e:
      self.log.error("Failed to register client with Hue Switch at %s with error '%s'" % (ip, e))
      return None

    # body = {:devicetype => "Hue_Switch"}
    #       create_user = HTTParty.post("http://#{@ip}/api", :body => body.to_json)
    #       if create_user.first.include?("error")
    #         raise "You need to press the link button on the bridge and run again"
    #       elsif create_user.first.include?("success")
    #         new_user = create_user.first["success"]["username"]
    #         @user = new_user
    #         File.write("alexa_hue_user","#{new_user}")
