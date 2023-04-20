#! /usr/bin/env sh

# Exit in case of error
set -e

watchmedo auto-restart -d first/ -p *.py -R -- python first/kektris.py
