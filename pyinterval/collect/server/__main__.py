from xmlrpc.server import SimpleXMLRPCServer
import os
from urllib.parse import urlparse
from .sqlite3 import SQLite3Server
import argparse
from pprint import pprint

'''
Command line tool to run db server.
'''

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--dbfile', type=str, default=os.path.join(os.getcwd(), "{}.sql".format(os.environ["USER"])),
                    help='The db file to use by this server. Defaults to $(pwd)/${USER}.sql')
parser.add_argument('--url', type=str, default="http://localhost:8000", help="URL of db server")

parser.add_argument('--verbose', action="store_true", default=False, help="show a lot of additional information (for debug purposes mainly)")

args = parser.parse_args()

parse_results = urlparse(args.url)

db_server = SQLite3Server(args.dbfile)

server = SimpleXMLRPCServer((parse_results.hostname, parse_results.port), allow_none=True)

print("Listening on", args.url)

if args.verbose:
    def emit(*args, **kwargs):
        db_server.emit(*args, **kwargs)
        print("**** current state ****")
        pprint(db_server._dump_db())
else:
    emit = db_server.emit

server.register_function(emit, "emit")

server.serve_forever()

