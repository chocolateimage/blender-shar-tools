#!/usr/bin/env bash

FILENAME="add-on-chocolateimage-blender-shar-tools-v1.0.0.zip"
cd src
cp ../LICENSE.md .
cp ../README.md .
rm ../$FILENAME
zip -r ../$FILENAME ./*
rm LICENSE.md
rm README.md
cd ..

echo "            \"archive_size\": $(stat -c%s "$FILENAME"),"
echo "            \"archive_hash\": \"sha256:$(sha256sum "$FILENAME" | cut -d " " -f 1)\""