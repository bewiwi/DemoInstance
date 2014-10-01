import ConfigParser

IMAGE_CONF_PREFIX='IMAGE_'


class DemoConfig():
    def __init__(self,config_file='./config.ini'):
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)
        self.user=self.config.get("OPENSTACK","user")
        self.password=self.config.get("OPENSTACK","password")
        self.tenant=self.config.get("OPENSTACK","tenant")
        self.url=self.config.get("OPENSTACK","url")
        if self.config.has_option("OPENSTACK","region"):
            self.region = self.config.get("OPENSTACK","region")
        else:
            self.region = None
        self.http_port=self.config.getint("HTTP","port")
        self.database_connection=self.config.get("DATABASE","connection")
        self.log_level=self.config.get("DEFAULT","log_level")

        self.images = {}
        for section in self.config.sections():
            if not section.startswith(IMAGE_CONF_PREFIX):
                continue
            image = DemoConfigImage()
            image.image_id = self.config.get(section, "image_id")
            image.name = self.config.get(section, "name")
            image.desc = self.exist_or_none(section, "desc")
            image.img = self.exist_or_none(section, 'img')
            image.info = self.exist_or_none(section, 'info')
            image.flavor_id = self.config.get(section,"flavor_id")
            image.instance_prefix = self.config.get(section,"prefix")
            image.instance_check_url = self.config.get(section,"check_url")
            image.instance_soft_url = self.config.get(section,"soft_url")
            image.instance_time = self.config.get(section,"time")
            image.max_instance = self.config.getint(section,"max_instance")
            key_name = section[len(IMAGE_CONF_PREFIX):]
            self.images[key_name] = image

    def exist_or_none(self,section,key):
        if self.config.has_option(section, key):
            return self.config.get(section,key)
        return None


class DemoConfigImage():
    def __init__(self):
        self.image_id = None
        self.flavor_id = None
        self.instance_prefix = None
        self.instance_check_url = None
        self.instance_soft_url = None
        self.instance_time = None
        self.max_instance = None
        self.name = None
        self.desc = None
        self.info = None