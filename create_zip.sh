#!/usr/bin/env bash

FILENAME="/tmp/add-on-chocolateimage-blender-shar-tools-v1.0.0.zip"
rm "$FILENAME"
zip -r "$FILENAME" ./*

echo "            \"archive_size\": $(stat -c%s "$FILENAME"),"
echo "            \"archive_hash\": \"sha256:$(sha256sum "$FILENAME" | cut -d " " -f 1)\""
