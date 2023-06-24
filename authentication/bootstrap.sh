#!/usr/bin/env sh

echo BOOTSTRAP STARTED
python bootstrap.py
echo BOOTSTRAP COMPLETED
python authentication.py