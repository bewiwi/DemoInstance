from Demo.demo_config import DemoConfig
from Demo.http import ThreadedHTTPServer, Handler
from Demo.vacuum import Vacuum
import logging

if __name__ == '__main__':
    config = DemoConfig()
    logging.basicConfig(level=config.log_level)
    vacuum = Vacuum()
    try:
        vacuum.start()
        server = ThreadedHTTPServer(('0.0.0.0', config.http_port), Handler)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        vacuum.stop = True
