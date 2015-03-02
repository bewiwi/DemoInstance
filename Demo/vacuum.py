from database import Instance
from demo_config import DemoConfig
from demo import Demo
import threading
import datetime
from time import sleep
import logging


class Vacuum(threading.Thread):
    def __init__(self):
        self.config = DemoConfig()
        self.stop = False
        threading.Thread.__init__(self)

    def check_old_instance(self):
        demo = Demo(self.config)
        database = demo.database

        logging.debug('CHECK OLD INSTANCE')
        query = database\
            .query(Instance)\
            .filter(Instance.status != 'DELETED')
        logging.debug("%s count", query.count())
        instances = demo.provider.get_instances()
        for data_instance in query.all():
            destroy_at = data_instance.launched_at\
                        + datetime.timedelta(
                            0, 0, 0, 0,
                            data_instance.life_time
                        )
            logging.debug(
                '%s must be destroy at %s',
                data_instance.openstack_id, destroy_at
            )
            if destroy_at < datetime.datetime.now():
                logging.info('%s is to old', data_instance.openstack_id)
                demo.database_remove_server(data_instance.openstack_id)

            on_cloud = False
            for id in instances:
                if data_instance.openstack_id == id:
                    on_cloud = True
                    break
            if not on_cloud and data_instance.openstack_id:
                logging.info(
                    '%s is not present on cloud anymore',
                    data_instance.id
                )
                demo.database_remove_server(data_instance.openstack_id)

    def run(self):
        time_between_vacuum = 60
        while True:
            try:
                self.check_old_instance()
            except Exception as e:
                logging.error("Vaccum Raise Execption %s", e.message)
            i = 0
            while i < time_between_vacuum:
                if self.stop:
                    logging.info('Stop vacuum')
                    return
                i += 1
                sleep(1)
        logging.error('Vacuum is stop')
