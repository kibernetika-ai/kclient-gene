#!/usr/bin/env bash

python3 prepare.py --source http://localhost:8082/docs/apidocs.json
rm -r out/go
java -jar swagger-codegen-cli.jar generate -c config.json -i prepared.json -l go -o out/go
libdir="$HOME/go/src/github.com/kibernetika-ai/go-kclient"
rm -r $libdir/pkg/kclient
mkdir $libdir/pkg/kclient
cp out/go/*.go $libdir/pkg/kclient/
cp assets/*.go $libdir/pkg/kclient/
cp -r out/go/docs $libdir/docs
cp out/go/*.md $libdir/