#!/usr/bin/env bash

cd src
cp ../LICENSE.md .
cp ../README.md .
rm ../add-on-chocolateimage-blender-shar-tools-v1.0.0.zip
zip -r ../add-on-chocolateimage-blender-shar-tools-v1.0.0.zip ./*
rm LICENSE.md
rm README.md
cd ..