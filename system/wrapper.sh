#!/bin/bash

python -m flask -A /app/system/main run -h 0.0.0.0 &
nice -20 ./metrics &

wait -n
exit $?