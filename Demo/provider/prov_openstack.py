from novaclient.client import Client
import logging
from prov import DemoProv


class Openstack(DemoProv):
    def __init__(self, config):
        self.user = config['user']
        self.password = config['password']
        self.tenant = config['tenant']
        self.url = config['url']
        if 'region' in config:
            self.region = config['region']
        else:
            self.region = None

        self.nova = Client(
            2, self.user, self.password,
            self.tenant, self.url,
            region_name=self.region
        )

    def get_instances(self):
        instances_id = []
        for instance in self.nova.servers.list():
            instances_id.append(instance.id)
        return instances_id

    def __get_instance_info(self, instance):
        return instance._info.copy()

    def __get_instance(self, id):
        for instance in self.nova.servers.list():
            if id == self.__get_instance_info(instance)['id']:
                return instance
        return False

    def instance_exist(self, id):
        for instance_id in self.get_instances():
            if instance_id == id:
                return True
        return False

    def instance_is_up(self, id):
        instance = self.__get_instance(id)
        if not instance:
            return False
        logging.info('Check started %s', instance)
        info = self.__get_instance_info(instance)
        if info['status'] == 'ACTIVE' \
                and info['OS-EXT-STS:task_state'] is None:
            return True
        else:
            return False

    def create_instance(self, image_conf):
        logging.debug("Image config : %s", image_conf.image_id)
        matches = self.nova.images.findall(name=image_conf.image_id)
        if len(matches) == 0:
            # If no match name check id
            image = self.nova.images.find(id=image_conf.image_id)
        else:
            # Get first name matching
            image = matches[0]
        logging.debug("Image id : %s", image.id)
        logging.debug("Flavor config : %s", image_conf.flavor_id)

        matches = self.nova.flavors.findall(name=image_conf.flavor_id)
        if len(matches) == 0:
            flavor = self.nova.flavors.find(id=image_conf.flavor_id)
        else:
            flavor = matches[0]

        logging.debug("Flavor id : %s", flavor.id)

        instance = self.nova.servers.create(
            image_conf.instance_prefix + 'test',
            image.id,
            flavor.id,
            userdata=image_conf.user_data
        )
        return self.__get_instance_info(instance)['id']

    def remove_instance(self, id):
        instance = self.__get_instance(id)
        instance.delete()

    def get_instance_ip(self, id):
        instance = self.__get_instance(id)
        info = self.__get_instance_info(instance)
        interfaces = info['addresses'].keys()
        return info['addresses'][interfaces[0]][0]['addr']
