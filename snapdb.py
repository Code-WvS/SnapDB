#!/usr/bin/env python3

from mongodict import MongoDict
from blockext import *
from config import config

class Storage:
    def __init__(self):
        self.db = MongoDict(
                host=config["host"], port=config["port"],
                database=config["database"], collection=config["collection"],
                auth=(config["username"], config["password"]))
    
    @predicate("%s from the database")
    def get(self, key):
        if key in self.db:
            return self.db[key]
        else:
            return ""

    @command("%s as %s into the database")
    def put(self, value, key):
        self.db[key] = value

descriptor = Descriptor(
    name = "SnapDB",
    port = config["localport"],
    blocks = get_decorated_blocks_from_class(Storage)
)

extension = Extension(Storage, descriptor)

if __name__ == "__main__":
    extension.run_forever(debug=True)
