from novaclient.client import Client


class Openstack():
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
            2, config.user, config.password,
            config.tenant, config.url,
            region_name=config.region
        )

    def get_instances(self):
        return self.nova.servers.list()

    def get_instance(self, id):
        for instance in self.get_instances():
            if id == self.get_instance_info(instance)['id']:
                return instance
        return False

