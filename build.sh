#!/bin/sh

# Change root of fronted
sed -i "s/http:\/\/localhost:5000\//$URL_DEPLOY/" frontend/src/main.js

# Generates build files for fronted
npm install --prefix frontend
npm run build --prefix frontend

# Moves build data to create deployment files
mkdir buildDev
mkdir buildDev/templates
cp frontend/dist/index.html buildDev/templates
cp frontend/dist/static -r buildDev
mkdir buildDev/resources
cp backend/resources/*.py -r buildDev/resources
mkdir buildDev/model
cp backend/model/*.py -r buildDev/model
mkdir buildDev/utils
cp backend/utils/*.py -r buildDev/utils
cp deployment/* -r buildDev
cp backend/*.py buildDev

# Removes original folders
rm -r frontend
rm -r backend
rm -r deployment

# Moves temporal data to root
find ./buildDev -maxdepth 1 -exec mv {} . \;

# Removes temporal build data
rm -r buildDev
# Remove shell file
rm build.sh