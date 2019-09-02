# Integrate LowPowerLab IoT Gateway GarageMote to be controlled via Amazon Echo Devices

## Project Summary:

This project enables the LowPowerLab GarageMote to be controlled via an Amazon Echo device.  I extended the IoT Gateway created by Felix Rusu (see Links below) to allow an Amazon Echo "Alexa" device to control the GarageMote.

## Equipment Needed
*Note: I wrote this project to support 2 GarageMotes, it could be easily be modified to support 1 or 3 (or more) doors.*
* 2 x LowPowerLab GarageMote
* 2 x LowPowerLab Moteino
* 1 x LowPowerLab MightyHat or Moteino (for base station)
* 1 x Raspberry Pi (for IoT Gateway)

## Details

In order to implement this project you should have an existing GarageMote operating via a LowPowerLab IoT Gateway (works with v9!).  To fully implement you will need to:
* Set up AWS IoT "Thing"
  * Link to a certificate and ensure you have saved private, public and root files
  * Copy the following files to /home/pi/certs/ :
    * Rename `<certID>-private.pem.key` to `garage-private.pem.key`
    * Rename `<certID>-certificate.pem.crt` to `garage-certificate.pem.crt`
    * Create `root-CA.crt` from the appropriate root cert
  * Alternately, you could change the file names in userMetrics/alexa_aws_iot.js file.
* Set up an Alexa Skill at developer.amazon.com
  * Sample Invocation, Intent and Slots Interaction model JSON in alexa folder
* Copy LowPowerLab_FileModes/userMetrics/alexa_aws_iot.js to /User/pi/userMetrics/ directory. 
* Modify settings.json5 to add additional settings - call out https://github.com/LowPowerLab/RaspberryPi-Gateway
  * Lines 134-153 were added to support the settings needed to connect to AWS 
* Deploy Python Code to AWS Lambda
  * Ensure you a VirtualEnv installed 
  * Ensure you have all requirements installed
  * Ensure you have run AWS Config and entered your AWS Key/Secret
  * Run `sh compress_lambda.sh` to push code to your Lambda
  * Declare Environmental Variables
    * IOT_ENDPOINT - your IoT Endpoint (example: xxxxxxxxxxx.iot.us-east-1.amazonaws.com)
    * THING_NAME - Name of thing in IoT (example: GarageDoor)
    * THING_TOPIC - Name of thing topic (example: /GarageDoor)
    
## IoT Gateway
* Install aws-iot-device-sdk
    * `npm install aws-iot-device-sdk`
* In the Garage Node setup https://<IP or FQDN>/#nodedetails
    * Add `Garage : AWSUpdate` as an Event

## Links:
* GarageMote: https://lowpowerlab.com/guide/garagemote/
* MightyHat: https://lowpowerlab.com/guide/mightyhat/
* LowPowerLab IoT Gateway: https://lowpowerlab.com/guide/gateway/

## Troubleshooting
* AWS Shadow is not updating.
    * Check that the certificate has a policy attached that allows the proper actions.  Example:
    `{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "iot:Publish",
            "iot:Subscribe",
            "iot:Connect",
            "iot:Receive"
          ],
          "Effect": "Allow",
          "Resource": [
            "*"
          ]
        }
      ]
    }`
* When I ask for garage door to report status, I get a response of "Large Garage door is null and small garage door is null"
    * The garage door names are currently hardcoded (yeah not the best) to use "large" and "small".  You also need to add an attribute to the AWS IoT shadow of "name" for example:
    `"node_42": {
          "type": "garage",
          "node_id": 42,
          "status": "closed",
          "last_updated": 1567448966256,
          "name": "small"
    }` 
