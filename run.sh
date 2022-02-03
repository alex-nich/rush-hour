#!/bin/sh

if [ "$#" -gt 1 ]; then
    ./rushhour.py "$1" "$2"
else
    ./rushhour.py "$1"
fi