#!/bin/sh
cp frontend/dist/index.html -r deployment/templates
cp frontend/dist/static -r deployment
cp backend/resources -r deployment
cp backend/model -r deployment
cp backend/*.py deployment
