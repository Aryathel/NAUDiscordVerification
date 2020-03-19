#!/bin/sh
clear
tempSleep() {
  for i in {5..1}
  do
    echo "$i"
    sleep 1
  done
}
while true do
  python main.py
  echo "Restarting in..."
  tempSleep()
