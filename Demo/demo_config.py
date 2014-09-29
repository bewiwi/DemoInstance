import ConfigParser

IMAGE_CONF_PREFIX='IMAGE_'


class DemoConfig():
    def __init__(self,config_file='./config.ini'):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.user=config.get("OPENSTACK","user")
        self.password=config.get("OPENSTACK","password")
        self.tenant=config.get("OPENSTACK","tenant")
        self.url=config.get("OPENSTACK","url")
        if config.has_option("OPENSTACK","region"):
            self.region = config.get("OPENSTACK","region")
        else:
            self.region = None
        self.http_port=config.getint("HTTP","port")
        self.database_connection=config.get("DATABASE","connection")
        self.log_level=config.get("DEFAULT","log_level")

        self.images = {}
        for section in config.sections():
            if not section.startswith(IMAGE_CONF_PREFIX):
                continue
            image = DemoConfigImage()
            image.image_id = config.get(section, "image_id")
            image.name = config.get(section, "name")
            image.desc = config.get(section, "desc")
            image.flavor_id = config.get(section,"flavor_id")
            image.instance_prefix = config.get(section,"prefix")
            image.instance_check_url = config.get(section,"check_url")
            image.instance_soft_url = config.get(section,"soft_url")
            image.instance_time = config.get(section,"time")
            image.max_instance = config.get(section,"max_instance")
            key_name = section[len(IMAGE_CONF_PREFIX):]
            self.images[key_name] = image


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