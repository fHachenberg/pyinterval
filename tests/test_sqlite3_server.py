from datetime import datetime

from pyinterval.collect.server.sqlite3 import SQLite3Server

def test_server():
    srv = SQLite3Server(":memory:")
    tstamp = datetime.strptime("2010-10-10 17:45:05", "%Y-%m-%d %H:%M:%S").timestamp()
    srv.emit("a", "b", timestamp=tstamp)
    assert srv._dump_db() == [(1286725505.0, 'a', 'b', None)]

