#!/bin/bash

wait_exit() {
  echo "Press enter to exit";
  read -r;
  exit;
}

## bot build section (nodejs-backend for managing the search-threads)
cd bot || wait_exit
npm i
npm run build || wait_exit
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cp ./.env ./build/.env # BEWARE !!! 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cd ..

## frontend build that uses the nodejs-backend
cd frontend || wait_exit
npm i
npm run build || wait_exit
cd ..

# building the docker-images and starting up all containers (all containers represent a part of the app)
docker compose up --build -d --scale scraper=3 || wait_exit
echo "Build Complete"

wait_exit