# Simple instrumentation of any command line tool: Simply define
# alias <tool>="pyinterval_instrument $@"
# in your .bashrc
# 
# The script only works if pyinterval is installed in the Python
# environment, e.g. ~/.local or system-wide (or whatever Python
# environment is active)

# Calls pyinterval.collect.client with $@ and pwd
from .client.__main__ import main as client_main
from subprocess import call
import os
import sys

def main(args=None) -> int:
    if args is None:
        args = sys.argv

    cwd = os.getcwd()
   
    cmdline = " ".join(args[1:])
   
    client_main([cmdline, "--workdir=" + cwd, "--start"])
    status = call(cmdline, shell=True)
    client_main([cmdline, "--workdir=" + cwd, "--stop"])
    return status

if __name__ == "__main__":
    status = main()
    raise SystemExit(status)
