#!/usr/bin/env python3

import sys
from os.path import abspath

sys.path.append(abspath('.'))
from romidata2.webapp import FarmWebApp
from romidata2.db import FarmDatabase
from romidata2.webcache import WebCache

if __name__ == "__main__":
    db = FarmDatabase("demo/db")
    cache = WebCache(db, "farms", "/tmp/romicache")
    app = FarmWebApp(db, cache)
    app.run(host='0.0.0.0')
