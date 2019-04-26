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
* Modify LowPowerLab metrics.js file - call out https://github.com/LowPowerLab/RaspberryPi-Gateway and add diff!
  * TODO: figure out how to present diff in Github/README
* Modify settings.json5 to add additional settings - call out https://github.com/LowPowerLab/RaspberryPi-Gateway and add diff!
  * TODO: Add example file... without any personal info!
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
