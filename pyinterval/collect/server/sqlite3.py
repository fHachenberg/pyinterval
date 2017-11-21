import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
import os
from contextlib import contextmanager

class SQLite3Server:
    '''
    allows logging of events into sqlite3 db

    Normally, each user uses its own DB file to allow for easy management via version control (svn, git)
    
    .. important::
    
        Should not be used directly. Please use managed_server instead, because the context manager
        automatically handles the cleanup. 
    '''
    def __init__(self, dbfile: str):
        if not os.path.exists(dbfile):
            setup = True
        else:
            setup = False

        self.conn = sqlite3.connect(dbfile)

        if setup:
            # setup database
            self.conn.execute('''CREATE TABLE events
                                 (timestamp real, task text, workdir text, start integer)''')

    def emit(self, task: str, workdir: str, start: Optional[bool] = None, timestamp: Optional[float] = None):
        '''
        Adds entry to log

        :param task: String describing the task (like "make a.out")
        :param workdir: The workdir this task is associated with
        :param start: if True, the task started. If False, the task stopped. If None, this is not an interval
        :param timestamp: The event time as POSIX timestamp. If not given, datetime.now().timestamp() is used
        :return:
        '''
        if timestamp is None:
            timestamp = datetime.now().timestamp()

        self.conn.execute("INSERT INTO events values (?, ?, ?, ?)", (timestamp, task, workdir, start))
        # We write changes to the file immediately to be on the safe side
        # This might get very slow for many logged events, so it might be necessary 
        # in the future to periodically commit or only commit on close!
        self.conn.commit()       

    def close(self):
        '''
        Must be the final action of the server object
        '''        
        self.conn.close()

    def _dump_db(self) -> List[Tuple[int, str, str, int]]:
        '''
        Returns current content of database for test purposes
        :return: List of entries
        '''
        c = self.conn.execute("SELECT * FROM events")
        return c.fetchall()
    
@contextmanager
def managed_server(dbfile: str):
    '''
    Context manager to setup server instance and close it appropriately in case of
    exceptions.
    '''
    server = SQLite3Server(dbfile)
    yield server
    server.close()
    