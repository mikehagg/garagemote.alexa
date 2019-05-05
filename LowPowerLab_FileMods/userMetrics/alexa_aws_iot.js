// ******************************************************************************************************************************************
//                                           AWS IOT INTEGRATION
// ******************************************************************************************************************************************
// init AWS-IOT Connection
// Helper function to send JSON updates to AWS IoT
// ******************************************************************************************************************************************

var awsIot = require('aws-iot-device-sdk');
thingName = settings.aws.aws_IOT_thing_name.value; // AWS IoT Thing Name

var device = awsIot.thingShadow({
    keyPath: '/home/pi/certs/garage.private.key',  // Download during AWS IoT Device creation
    certPath: '/home/pi/certs/garage.cert.pem',  // Download during AWS IoT Device creation
    caPath: '/home/pi/certs/root-CA.crt',  // Download during AWS IoT Device creation
    clientId: settings.aws.aws_IOT_client_name.value, // Should be a unique Client name.
    host: settings.aws.aws_IOT_endpoint.value, // Set AWS IOT Endpoint in settings.json5
    region: settings.aws.aws_region.value,
    port: 8883
});

function sendData(thing, state) {
    console.log('Sending Data..', state);

    var clientTokenUpdate = device.update(thing, state);
    if (clientTokenUpdate === null) {
        console.log('Shadow update failed, operation still in progress');
    }
    else {
        console.log('Shadow update success.');
    }
};

device.on('delta', function (thingName, stateObject) {
    console.log('received delta on ' + thingName + ': ' + JSON.stringify(stateObject));
    for (var key in stateObject['state']) {

        var node = key.split("_")[1];
        var desired_state = stateObject['state'][key]['status'];

        console.log("Node: " + node + " desired state: " + desired_state);

        // Take action on garage door
        if (desired_state == 'open')
        {
            var action = "OPN";
        }
        else if (desired_state == 'closed')
        {
            var action = "CLS"
        }
        sendMessageToNode({"nodeId": parseInt(node), "action": action});

        // TODO resetting desired may be an issue for something like a thermostat, but is good for a garage!
        var resetDesiredState = {
            "state": {
                "desired": {
                    [key]: null
                }
            }
        };
        console.log("Desired State processed, sending to clear desired state: " + JSON.stringify(resetDesiredState));
        sendData(thingName, resetDesiredState);
    }
});

exports.events = {
    // **********************************************************************************************
    //                                  AWS Shadow Update
    // Written by: Mike Haggerty
    // Date: April 20, 2019
    //
    // **********************************************************************************************
    garageAWSShadowUpdate: {
        label: 'Garage : AWSUpdate',
        icon: 'comment',
        descr: 'Update AWS IoT Shadow',
        serverExecute: function (node) {
            if (node.metrics['Status'] && (Date.now() -
                new Date(node.metrics['Status'].updated).getTime() < 2000))
            {
                var key = 'node_' + node._id;
                var garageState = {
                    "state":
                        {
                            "reported":
                                {
                                    [key]:
                                        {
                                            "type": "garage",
                                            "node_id": node._id,
                                            "status": node.metrics['Status'].value.toLowerCase(),
                                            "last_updated": Date.now()
                                        }
                                }
                        }
                };
                console.log('Attempting to update AWS shadow with: ' + JSON.stringify(garageState));
                device.register(thingName, {}, function () {
                    console.log('Registered.');
                    sendData(thingName, garageState);
                });
                sendData(thingName, garageState);
                console.log('Successfully update AWS shadow.');
            }
        }
    }
    // ************************** END AWS Shadow Update **********************************************
}