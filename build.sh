#!/bin/sh
cp frontend/dist/index.html deployment/templates
cp frontend/dist/static -r deployment
cp backend/resources -r deployment
cp backend/model -r deployment
cp backend/utils -r deployment
cp backend/*.py deployment
