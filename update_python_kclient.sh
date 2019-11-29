#!/usr/bin/env bash

python3 prepare.py --source http://localhost:8082/docs/apidocs.json
rm -r out/python
java -jar swagger-codegen-cli.jar generate -c config.json -i prepared.json -l python -o out/python
rm -r ../python-kclient/kclient/api ../python-kclient/kclient/models ../python-kclient/docs
cp -r out/python/kclient/api ../python-kclient/kclient/api
cp -r out/python/kclient/models ../python-kclient/kclient/models
cp -r out/python/kclient/*.py ../python-kclient/kclient
cp -r out/python/docs ../python-kclient/docs
cp -r out/python/*.md ../python-kclient