from database import DemoData,Instance
from demo_config import DemoConfig
from demo import Demo
import threading
import datetime
from time import sleep
import logging


class Vacuum(threading.Thread):
    def __init__(self):
        self.config = DemoConfig()
        self.demo = Demo(self.config)
        self.database = self.demo.database
        self.stop = False
        threading.Thread.__init__(self)

    def check_old_instance(self):
        logging.debug('CHECK OLD INSTANCE')
        query = self.database.session.query(Instance).filter(Instance.status != 'DELETED')
        instances = self.demo.get_instances()
        for data_instance in query.all():
            destroy_at = data_instance.launched_at + datetime.timedelta(0, 0, 0, 0, data_instance.life_time)
            if destroy_at < datetime.datetime.now():
                logging.info('%s is to old',data_instance.id)
                self.demo.database_remove_server(data_instance)
            on_cloud = False
            for instance in instances:
                info = self.demo.get_instance_info(instance)
                if data_instance.id == info['id']:
                    on_cloud = True
            if on_cloud == False:
                logging.info('%s is not present on cloud',data_instance.id)
                self.demo.database_remove_server(data_instance)

    def run(self):
        while not self.stop:
            self.check_old_instance()
            sleep(60)