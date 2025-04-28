#!/bin/sh

echo "Loading data..."
yarn cli:dev load:data

echo "Starting server..."
yarn start:prod 