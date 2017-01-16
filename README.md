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

Intent `MirrorShowHideModuleIntent` allows the showing or hiding of individual modules. It can be activated with the command `Alexa, ask Aeneas to [show | hide] the [module name | everything]`. For example, `Alexa, ask Aeneas to hide the calendar` would result in the calendar being hidden and `Alexa, ask Aeneas to hide everything` would result in everything being hidden.

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

## Integrating with Alexa

To make Alexa call out to Aeneas you will need to create two things. First is the actual Skill on https://developer.amazon.com and the second is an Amazon Web Services Lambda function on https://aws.amazon.com.

This requires an Amazon developer account (free) and the specific steps are still to be filled in. However, the pertinant information is included below. I'll fill out the rest at a later date.

In short, your Alexa/Echo sends a request to the Amazon Skill which sends a request to the AWS Lambda which sends a request to the Aeneas instance which returns a response.

### Amazon Alexa Skill

The creation of an Alexa Skill will provide you with a skill id which is necessary for the Lambda discussed below. In the Configuration tab you will tell it to call out to an AWS Lambda and provide the lambda id.

##### Intent Schema
```
{
  "intents": [
    {
      "intent": "AMAZON.StopIntent"
      
    },
    {
      "intent": "AMAZON.CancelIntent"
      
    },
    {
      "intent": "MirrorShowHideModuleIntent",
      "slots":[
        {
          "name": "Module",
          "type": "MODULES"
        },
        {
          "name": "Action",
          "type": "ACTIONS"
        }
      ]
    },
    {
      "intent": "MirrorOnOffIntent",
      "slots":[
        {
          "name": "State",
          "type": "STATES"
        }
      ]
    }
  ]
}
```

##### Custom Slots
```
ACTIONS : show | hide
MODULES : clock | calendar | nest | weather | forecast | news | everything 
STATES  : on | off
```

##### Sample Utterances
```
MirrorShowHideModuleIntent {Action} {Module}
MirrorShowHideModuleIntent to {Action} {Module}
MirrorShowHideModuleIntent {Action} the {Module}
MirrorShowHideModuleIntent to {Action} the {Module}
MirrorOnOffIntent {State}
MirrorOnOffIntent mirror {State}
```

### Amazon Web Services Lambda

This makes use of a Lambda in Amazon Web Services to send web requests down to the running Aeneas instance.

```
var http = require('http');
var URLParser = require('url');
 
exports.handler = function (json, context) {
    try {
        // A list of URL's to call for each applicationId
        var handlers = {
            'appId':'url',
            '[your-alexa-skill-id]':'[your-ip-or-some-url-to-your-ip]:[aeneas-port]/aeneas'
        };
        
        // Look up the url to call based on the appId
        var url = handlers[json.session.application.applicationId];
        if (!url) { context.fail("No url found for application id"); }
        var parts = URLParser.parse(url);
        
        var post_data = JSON.stringify(json);
        
        // An object of options to indicate where to post to
        var post_options = {
            host: parts.hostname,
            auth: parts.auth,
            port: (parts.port || 80),
            path: parts.path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': post_data.length
            }
        };
        // Initiate the request to the HTTP endpoint
        var req = http.request(post_options,function(res) {
            var body = "";
            // Data may be chunked
            res.on('data', function(chunk) {
                body += chunk;
            });
            res.on('end', function() {
                // When data is done, finish the request
                context.succeed(JSON.parse(body));
            });
        });
        req.on('error', function(e) {
            context.fail('problem with request: ' + e.message);
        });
        // Send the JSON data
        req.write(post_data);
        req.end();        
    } catch (e) {
        context.fail("Exception: " + e);
    }
};
```

