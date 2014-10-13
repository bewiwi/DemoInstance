from novaclient.client import Client
from database import DemoData, Instance, User
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

    def get_instance_type(self,instance):
        info = self.get_instance_info(instance)
        query = self.database.session.query(Instance).filter(
            Instance.openstack_id == info['id']
        )
        data_instance = query.first()
        return data_instance.image_key

    def get_instance_soft_address(self,instance):
        return self.placeholder_apply(
            self.config.images[self.get_instance_type(instance)].instance_soft_url,
            instance)

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
        return int(self._get_total_seconds(delta)/60)

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

    def create_instance(self, image_key, time=None, token=None):
        logging.info("Create Instance")
        logging.debug("Image id : %s", self.config.images[image_key].image_id)
        logging.debug("Flavor id : %s", self.config.images[image_key].flavor_id)

        #Add a demand
        database_instance = Instance()
        database_instance.status = 'ASK'
        database_instance.launched_at = datetime.datetime.now()
        database_instance.life_time = 10
        database_instance.image_key = image_key
        database_instance.token = '0'
        self.database.session.add(database_instance)
        self.database.session.commit()

        raise_exception = False
        if self.database_count_active_instance(image_key) <= self.config.images[image_key].max_instance:
            new_instance = self.nova.servers.create(
                self.config.images[image_key].instance_prefix + 'test',
                self.config.images[image_key].image_id,
                self.config.images[image_key].flavor_id
            )
            life_time = self.config.images[image_key].instance_time
            if time is not None and self.config.images[image_key].instance_time_max is not None:
                #Check the defined time is good or hack attempt
                if time <= self.config.images[image_key].instance_time_max:
                    life_time = time
                else:
                    raise_exception = DemoExceptionInvalidImageTime(time)
        else:
            raise_exception = DemoExceptionToMuchInstance()

        if not raise_exception:
            #No Exception go create instance
            self.database_insert_server(new_instance, status='CREATED',
                                        life_time=life_time,
                                        image_key=image_key, token=token)

        #Remove the demand
        self.database.session.delete(database_instance)
        self.database.session.commit()

        if raise_exception:
            raise raise_exception

        return self.get_instance_info(new_instance)['id']

    def check_system_up(self, instance):
        ip = self.get_instance_ip(instance)

        url = self.placeholder_apply(
            self.config.images[self.get_instance_type(instance)].instance_check_url,
            instance)

        try:
            code = urllib2.urlopen(url).getcode()
        except:
            return False

        if code == 200:
            self.database_insert_server(instance, 'DONE')
            return True
        return False

    def database_insert_server(self, instance, status=None, life_time=None,image_key=None, token=None):
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

        if image_key:
            data_instance.image_key = image_key

        if life_time is not None:
            data_instance.life_time = life_time

        if token is not None:
            data_instance.token = token

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

    def database_count_active_instance(self, image_key):
        query = self.database.session.query(Instance).filter(
            Instance.status != 'DELETED',
            Instance.image_key == image_key
        )
        logging.debug('%s actives instances for %s', query.count(),image_key)
        return query.count()

    def create_user(self, email=None):
        user = User()
        user.email = email
        user.generate_token()
        user.last_connection = datetime.datetime.now()

        self.database.session.merge(user)
        self.database.session.commit()
        return user

    def get_user_by_token(self, token):
        query = self.database.session.query(User).filter(
            User.token == token
        )

        if query.count() == 0:
            return False

        user = query.first()
        user.last_connection = datetime.datetime.now()

        self.database.session.merge(user)
        self.database.session.commit()
        return user

    def placeholder_apply(self, param, instance):
        param = param.replace("%ip%", self.get_instance_ip(instance))
        return param

    #Python 2.6 hook
    def _get_total_seconds(self, td):
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6