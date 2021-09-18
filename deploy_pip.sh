#!/bin/zsh

rm Pipfile
rm Pipfile.lock
pip install google-api-python-client oauth2client
zip -r lambda_function.zip *
