# -*- coding: utf-8 -*-
'''HomeServer with RM mini3 a.k.a. BlackBean

Copyright (c) 2018 Daisuke IMAI

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''
import json
from tornado.ioloop import IOLoop
from tornado_json.routes import get_routes
from tornado_json.application import Application


def make_app():
    import blackbean
    routes = get_routes(blackbean)
    print("Routes\n=======\n\n" +
            json.dumps([(url, repr(rh)) for url, rh in routes], indent=2)
    )
    settings = {"debug":True }
    return Application(routes=routes, settings=settings, generate_docs=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.instance().start()
