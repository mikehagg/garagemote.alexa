#!/usr/bin/env bash
# Script to compress and push to AWS Lambda
# Ensure you have successfully run 'aws configure' to enter Access Key and Secret Access Key values.
# ********************************************************************************************
# Copyright Mike Haggerty (2019)
# Feel free to shameless steal, but please apply credit where credit is due!
# ********************************************************************************************
rm function.zip
cd venv/lib/python3.7/site-packages/
zip -r9 ../../../../function.zip .
cd ../../../..
zip -g function.zip main.py
zip -g function.zip modules/*
zip -g function.zip templates/*
aws lambda update-function-code --function-name 2019-pyGarageDoor --zip-file fileb://function.zip
