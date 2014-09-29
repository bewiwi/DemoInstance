from novaclient.client import Client
from database import DemoData, Instance
import logging
from pprint import pprint
import urllib2
import datetime
from demo_exception import *


class Demo():
    def __init__(self, config):
        self.config = config
        self.database = DemoData(self.config)
        self.nova = Client(
            2, config.user, config.password,
            config.tenant, config.url,
            region_name=config.region
        )

    def get_instance_info(self, instance):
        return instance._info.copy()

    def get_instance_ip(self,instance):
        info = self.get_instance_info(instance)
        interfaces = info['addresses'].keys()
        return info['addresses'][interfaces[0]][0]['addr']

    def get_instance_soft_address(self,instance):
        return self.placeholder_apply(self.config.instance_soft_url,instance)

    def get_instance_life_time(self, instance):
        info = self.get_instance_info(instance)
        query = self.database.session.query(Instance).filter(
            Instance.openstack_id == info['id']
        )
        data_instance = query.first()
        delta = (
            data_instance.launched_at
            + datetime.timedelta(0, 0, 0, 0, data_instance.life_time)
        ) - datetime.datetime.now()
        return int(delta.total_seconds()/60)

    def get_instances(self):
        return self.nova.servers.list()

    def get_instance(self, id):
        for instance in self.get_instances():
            if id == self.get_instance_info(instance)['id']:
                return instance
        return False

    def instance_is_up(self, instance):
        logging.info('Check started %s', instance)
        info = self.get_instance_info(instance)
        if info['status'] == 'ACTIVE' \
                and info['OS-EXT-STS:task_state'] is None:
            self.database_insert_server(instance, 'UP')
            return True
        else:
            return False

    def create_instance(self):
        logging.info("Create Instance")
        logging.debug("Image id : %s", self.config.image_id)
        logging.debug("Flavor id : %s", self.config.flavor_id)

        #Add a demand
        database_instance = Instance()
        database_instance.status = 'ASK'
        database_instance.launched_at = datetime.datetime.now()
        database_instance.life_time = 10

        self.database.session.add(database_instance)
        self.database.session.commit()

        raise_exception = False
        if self.database_count_active_instance() <= self.config.max_instance:
            new_instance = self.nova.servers.create(self.config.instance_prefix + 'test',
                                                self.config.image_id,
                                                self.config.flavor_id)
            self.database_insert_server(new_instance, 'CREATED', self.config.instance_time)
        else:
            raise_exception = True

        #Remove the demand
        self.database.session.delete(database_instance)
        self.database.session.commit()

        if raise_exception:
            raise DemoExceptionToMuchInstance()

        return self.get_instance_info(new_instance)['id']

    def check_system_up(self, instance):
        ip = self.get_instance_ip(instance)
        url = self.placeholder_apply(self.config.instance_check_url,instance)

        try:
            code = urllib2.urlopen(url).getcode()
        except:
            return False

        if code == 200:
            self.database_insert_server(instance, 'DONE')
            return True
        return False

    def database_insert_server(self, instance, status=None, life_time=None):
        info = self.get_instance_info(instance)
        logging.debug('Insert instance %s', info['id'])

        query = self.database.session.query(Instance).filter(
            Instance.openstack_id == info['id']
        )

        if query.count() > 0:
            data_instance = query.first()
        else:
            data_instance = Instance()
            data_instance.launched_at = datetime.datetime.now()

        data_instance.openstack_id = info['id']
        data_instance.status = status

        if info.has_key('name'):
            data_instance.name = info['name']

        if life_time is not None:
            data_instance.life_time = life_time

        self.database.session.merge(data_instance)
        self.database.session.commit()
        return data_instance

    def database_remove_server(self, database_instance):
        logging.info('DELETE instance %s', database_instance.openstack_id)

        # nova
        instance = self.get_instance(database_instance.openstack_id)
        if instance:
            instance.delete()
        else:
            logging.debug('Instance %s not in cloud',database_instance.openstack_id)

        #database
        database_instance.status = 'DELETED'
        self.database.session.merge(database_instance)
        self.database.session.commit()

    def database_count_active_instance(self):
        query = self.database.session.query(Instance).filter(
            Instance.status != 'DELETED'
        )
        logging.debug('%s actives instances', query.count())
        return query.count()

    def placeholder_apply(self, param, instance):
        param = param.replace("%ip%", self.get_instance_ip(instance))
        return param