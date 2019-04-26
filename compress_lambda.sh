#!/usr/bin/env bash
rm function.zip
cd venv/lib/python3.7/site-packages/
zip -r9 ../../../../function.zip .
cd ../../../..
zip -g function.zip main.py
zip -g function.zip modules/*
zip -g function.zip templates/*
aws lambda update-function-code --function-name 2019-pyGarageDoor --zip-file fileb://function.zip
