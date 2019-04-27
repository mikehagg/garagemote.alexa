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

In order to implement this project you should have an existing GarageMote operating via a LowPowerLab IoT Gateway.  To fully implement you will need to:
* Set up AWS IoT "Thing"
  * Link to a certificate and ensure you have saved private, public and root files
* Set up an Alexa Skill at developer.amazon.com
  * Sample Invocation, Intent and Slots Interaction model JSON in alexa folder
* Copy LowPowerLab_FileModes metrics.js to Gateway directory. 
  * Alternately you could copy the appropriate changes into your metrics.js file.
    * Lines 29-93 control reading and writing to AWS IoT thing.  There is also a listener that will detect when the desired  shadow state does not match the reported shadow state
    * Lines 300-340 defines the event that is triggered when the IoT gateway detects a state change in the Garage Door.
* Modify settings.json5 to add additional settings - call out https://github.com/LowPowerLab/RaspberryPi-Gateway
  * Lines 134-153 were added to support the settings needed to connect to AWS 
* Deploy Python Code to AWS Lambda
  * Ensure you a VirtualEnv installed 
  * Ensure you have all requirements installed
  * Ensure you have run AWS Config and entered your AWS Key/Secret
  * Run `sh compress_lambda.sh` to push code to your Lambda
  * Declare Environmental Variables
    * Variables Here

## Links:
* GarageMote: https://lowpowerlab.com/guide/garagemote/
* MightyHat: https://lowpowerlab.com/guide/mightyhat/
* LowPowerLab IoT Gateway: https://lowpowerlab.com/guide/gateway/
