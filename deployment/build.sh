#!/usr/bin/env bash

cd ..
cd web-ui
npm run build
cd ..
docker build -f deployment/Dockerfile -t turbo-fishstick .
