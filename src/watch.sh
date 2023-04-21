#! /usr/bin/env sh

# Exit in case of error
set -e

watchmedo auto-restart -d app/ -p *.py -R -- python app/kektris.py
