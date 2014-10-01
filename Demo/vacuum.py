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
        logging.debug("%s count",query.count())
        instances = self.demo.get_instances()
        for data_instance in query.all():
            destroy_at = data_instance.launched_at + datetime.timedelta(0, 0, 0, 0, data_instance.life_time)
            logging.debug('%s must be destroy at %s', data_instance.openstack_id ,destroy_at)
            if destroy_at < datetime.datetime.now():
                logging.info('%s is to old',data_instance.openstack_id)
                self.demo.database_remove_server(data_instance)

            on_cloud = False
            for instance in instances:
                info = self.demo.get_instance_info(instance)
                if data_instance.openstack_id == info['id']:
                    on_cloud = True
                    break
            if not on_cloud and data_instance.openstack_id:
                logging.info('%s is not present on cloud anymore',data_instance.id)
                self.demo.database_remove_server(data_instance)
        self.database.session.close()

    def run(self):
        time_between_vacuum = 60
        while True:
            self.check_old_instance()
            i=0
            while i < time_between_vacuum:
                if self.stop:
                    logging.info('Stop vacuum')
                    return
                i += 1
                sleep(1)
        logging.error('Vacuum is stop')
