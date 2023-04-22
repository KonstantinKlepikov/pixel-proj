#! /usr/bin/env sh

# Exit in case of error
set -e

watchmedo auto-restart -d kektris/ -p *.py -R -- python src/main.py
