#!/bin/zsh

pipenv install
rm -rf dist
mkdir dist
cp -r index.py dist
cp -r ga.py dist
cp -r .env dist
cp -r key_file.json dist
pipenv lock -r > requirements.txt
pip install -r requirements.txt -t dist
cd dist
zip -r ../lambda_function.zip *
cd ..
rm requirements.txt
