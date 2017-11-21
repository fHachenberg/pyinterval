#!/bin/bash

# Simple instrumentation of any command line tool: Simply define
# alias <tool>="pyinterval_instrument.sh $@"
# in your .bashrc
# 
# The script only works if pyinterval is installed in the Python
# environment, e.g. ~/.local or system-wide (or whatever Python
# environment is active)

# Calls pyinterval.collect.client with $@ and pwd
python -m pyinterval.collect.client "$*" --workdir $(pwd) --start
$@
status=$?
python -m pyinterval.collect.client "$*" --workdir $(pwd) --stop
exit $status
