# Aeneas - Amazon Alexa Skill Handler

Aeneas functions as a set of controllers where each handles actions for a particular item. For example, the [MirrorController](src/main/python/controllers/mirror/mirror_controller.py) handles actions for a [MagicMirror](https://github.com/MichMich/MagicMirror).

## Aeneas Startup

When Aeneas starts it will do two things. First, it starts a [Flask](http://flask.pocoo.org) application listening on the provided port using [FlaskAsk](https://github.com/johnwheeler/flask-ask), which is a library built specifically to assist making Alexa handlers in python. Second, it creates instances of each registered Controller. That's it. The expectation is that each Controller registers the Alexa Intents that they are listening for and handling.

Aeneas is most easily started by navigating to the `src/main/python` directory and running 

`python aeneas.py -p <port>`

Run with `-h` to see all startup options.

## Controllers

A Controller's job is to handle actions for a particular item. It does this by registering with FlaskAsk the Alexa Intents it wishes to listen for and handle. 

### Mirror Controller

The MirrorController exists to control a MagicMirror and supports showing or hiding any or all modules running on the mirror. Upon startup it will register two intents, one for module control and one for turning the mirror on or off. This controller, as currently coded, is assuming that there is a MagicMirror running on the same host on port 8080.

#### Module Control

Intent `MirrorShowHideModuleIntent` allows the showing or hidding of individual modules. It can be activated with the command `Alexa, ask Aeneas to [show | hide] the [module name | everything]`. For example, `Alexa, ask Aeneas to hide the calendar` would result in the calendar being hidden and `Alexa, ask Aeneas to hide everything` would result in everything being hidden.

#### On/Off Control

Intent `MirrorOnOffIntent` allows the turning on or off of the mirror. All it is actually doing is showing or hiding everything. It can be activated with command `Alexa, ask Aeneas to turn the mirror off`.

#### Registered Modules

As coded now, the supported mirror modules are hard-coded to their known module ids. The list is

```
"clock" : "module_0_clock"
"calendar" : "module_1_calendar"
"forecast" : "module_4_weatherforecast"
"nest" : "module_5_MMM-Nest"
"news" : "module_6_newsfeed"
"weather" : "module_3_currentweather"
```

The module ids can be found by calling the MagicMirror endpoint at `http://localhost:8080/remote?action=MODULE_DATA`. I do intend to enhance the mirror so that you can register the module names there and just request a list of all running modules with friendly names. At the moment, I do not believe that is possible.

### Hue Controller

The HueController is intended to control Hue lights. It is currently not complete or at all usable.

