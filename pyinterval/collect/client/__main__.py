import os
import argparse
from datetime import datetime
import xmlrpc.client

'''
Command line tool to add event to running db server.
'''

def main(args=None):

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('task', type=str, help='String describing the task (like "make a.out")')
    parser.add_argument('--workdir', type=str, default=os.getcwd(), help='The workdir this task is associated with. If not given, `cwd` is assumed')
    parser.add_argument('--start', dest="start", action="store_true", default=None, help='mark event as start of task')
    parser.add_argument('--stop', dest="start", action="store_false", help='mark event as stop of task')
    parser.add_argument('--timestamp', type=str, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), help='date and time of event. Format "Y-m-d H:M:S". If not given, `now` is assumed')

    parser.add_argument('--server', type=str, default="http://localhost:8000", help="URL of db server")

    args = parser.parse_args(args)

    with xmlrpc.client.ServerProxy(args.server, allow_none=True) as proxy:
        proxy.emit(args.task, args.workdir, args.start, datetime.strptime(args.timestamp, "%Y-%m-%d %H:%M:%S").timestamp())

if __name__ == "__main__":
    main()