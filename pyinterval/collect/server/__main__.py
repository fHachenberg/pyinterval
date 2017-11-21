from xmlrpc.server import SimpleXMLRPCServer
import os
from urllib.parse import urlparse
from .sqlite3 import managed_server
import argparse
from pprint import pprint

'''
Command line tool to run db server.
'''
def main(args=None):

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dbfile', type=str, default=os.path.join(os.getcwd(), "{}.sql".format(os.environ["USER"])),
                        help='The db file to use by this server. Defaults to $(pwd)/${USER}.sql')
    parser.add_argument('--url', type=str, default="http://localhost:8000", help="URL of db server")
    parser.add_argument('--verbose', action="store_true", default=False, help="show a lot of additional information (for debug purposes mainly)")

    args = parser.parse_args(args)

    parse_results = urlparse(args.url)

    # handles cleanup on KeyboardInterrupt and other exceptions
    with managed_server(args.dbfile) as db_server:

        server = SimpleXMLRPCServer((parse_results.hostname, parse_results.port), allow_none=True)

        print("Listening on", args.url)

        if args.verbose:
            # declare wrapper function which outputs server state
            # after each event
            def emit(*args, **kwargs):
                db_server.emit(*args, **kwargs)
                print("**** current state ****")
                pprint(db_server._dump_db())
        else:
            emit = db_server.emit

        server.register_function(emit, "emit")

        server.serve_forever()

if __name__ == "__main__":
    main()
    