#!/bin/bash
set -x
PID_FILE=/var/run/eng-kn-bot.pid
kill -9 `cat $PID_FILE`
