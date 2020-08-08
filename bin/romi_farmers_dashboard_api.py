#!/usr/bin/env python3

import sys
from os.path import abspath

import argparse

sys.path.append(abspath('.'))
from romidata2.webapp import FarmWebApp
from romidata2.db import FarmDatabase
from romidata2.webcache import WebCache

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the REST server")
    parser.add_argument("-d", "--db", required=True,
                        help="The path of the database directory")
    parser.add_argument("-c", "--cache", required=True,
                        help="The path to the web cache directory")
    parser.add_argument("-t", "--type", required=True,
                        help="Either 'farms' or 'investigations'")
    
    args = parser.parse_args()
    db = FarmDatabase(args.db)
    cache = WebCache(db, args.type, args.cache)
    app = FarmWebApp(db, cache)
    app.run(host='0.0.0.0')
