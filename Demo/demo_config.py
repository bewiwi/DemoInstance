import ConfigParser


class DemoConfig:
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
        self.image_id=config.get("INSTANCE","image_id")
        self.flavor_id=config.get("INSTANCE","flavor_id")
        self.instance_prefix=config.get("INSTANCE","prefix")
        self.instance_check_url = config.get("INSTANCE","check_url")
        self.instance_soft_url = config.get("INSTANCE","soft_url")
        self.instance_time = config.get("INSTANCE","time")
        self.max_instance = config.get("INSTANCE","max_instance")
        self.http_port=config.getint("HTTP","port")
        self.database_connection=config.get("DATABASE","connection")
        self.log_level=config.get("DEFAULT","log_level")