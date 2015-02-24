#!/usr/bin/env python3
import sys
from mongodict import MongoDict
from blockext import *

PORT=4345

class Storage:
    def __init__(self):
        self.disconnect()

    @reporter("connect as user %s with password %s to database (host %s , port %n , database %s , collection %s )", defaults=["", "", "localhost", 27017, "snapmesh", "snapmesh"])
    def connect(self, username, password, host, port, database, collection):
        try:
            self.db = MongoDict(host, port, database, collection, auth=(username, password))
            return "ok"
        except:
            return "error: " + str(sys.exc_info()[1])

    @command("disconnect")
    def disconnect(self):
        self.db = None

    @predicate("connected?")
    def is_connected(self):
        return self.db is not None

    @reporter("%s from the collection")
    def get(self, key):
        if self.db is None:
            return "not connected"

        if key in self.db:
            return self.db[key]
        else:
            return ""

    @command("%s as %s into the collection")
    def put(self, value, key):
        if self.db is None:
            return "not connected"

        self.db[key] = value

    @reporter("contents of the collection")
    def list(self):
        if self.db is None:
            return "not connected"

        return "\n".join(self.db.keys())

descriptor = Descriptor(
    name="SnapDB",
    port=PORT,
    blocks=get_decorated_blocks_from_class(Storage)
)

extension = Extension(Storage, descriptor)

if __name__ == "__main__":
    extension.run_forever(debug=True)
