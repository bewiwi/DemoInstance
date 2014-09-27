from Demo.demo_config import DemoConfig
from Demo.http import ThreadedHTTPServer,Handler
from Demo.vacuum import Vacuum
from Demo.demo import Demo
from Demo.database import DemoData
import logging

if __name__ == '__main__':
    config = DemoConfig()
    logging.basicConfig(level=config.log_level)
    ###
    demo = Demo(config)
    demo.create_instance()
    ###
    vacuum = Vacuum()
    try:
        vacuum.start()
    except (KeyboardInterrupt, SystemExit):
        vacuum.stop = True

    server = ThreadedHTTPServer(('0.0.0.0', config.http_port), Handler)
    server.serve_forever()