#!/bin/bash

wait_exit() {
  echo "Press enter to exit";
  read -r;
  exit;
}

cd bot || wait_exit
npm i
npm run build || wait_exit
cp ./.env ./build/.env
cd ..

cd frontend || wait_exit
npm i
npm run build || wait_exit
cd ..

docker compose up --build -d --scale scraper=3 || wait_exit
echo "Build Complete"

wait_exit