from Demo.demo_config import DemoConfig
from Demo.http import ThreadedHTTPServer, Handler
from Demo.vacuum import Vacuum
import logging
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='config file', default='./config.ini')
    args = parser.parse_args()

    DemoConfig.config_file = args.c
    config = DemoConfig()
    logging.basicConfig(level=config.log_level)
    vacuum = Vacuum()
    try:
        vacuum.start()
        server = ThreadedHTTPServer(('0.0.0.0', config.http_port), Handler)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        vacuum.stop = True
