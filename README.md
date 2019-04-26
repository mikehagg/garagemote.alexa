# Integrate LowPowerLab IoT Gateway GarageMote to be controlled via Amazon Echo Devices

## Project Summary:

This project enables the LowPowerLab GarageMote to be controlled via an Amazon Echo device.  I extended the IoT Gateway created by Felix Rusu (see Links below) to allow an Amazon Echo "Alexa" device to control the GarageMote.

## Equipment Needed
* Raspberry Pi
* 2 x LowPowerLab GarageMote
* 2 x LowPowerLab Moteino
* 1 x LowPowerLab MightyHat or Moteino (for base station)

## Details

In order to implement this project you should have an existing GarageMote operating via a LowPowerLab IoT Gateway.  To fully implement you will need to:
* Set up AWS IoT "Thing"
  * Link to a certificate and ensure you have saved private, public and root files
* Set up an Alexa Skill at developer.amazon.com
  * Sample Invocation, Intent and Slots Interaction model JSON in alexa folder
* Modify LowPowerLab metrics.js file
  * TODO: figure out how to present diff in Github/README
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
