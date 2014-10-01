import ConfigParser
from copy import copy
from demo_exception import DemoExceptionInvalidImage

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
        template_image = self.get_image_by_section('IMAGE')
        for section in self.config.sections():
            if not section.startswith(IMAGE_CONF_PREFIX):
                continue
            image = self.get_image_by_section(section, template_image=template_image)
            key_name = section[len(IMAGE_CONF_PREFIX):]
            image.check()
            self.images[key_name] = image

    def get_image_by_section(self, section, template_image=None):
        if template_image is None:
            image = DemoConfigImage()
        else:
            image = copy(template_image)
        if self.config.has_option(section, "image_id"):
            image.image_id = self.config.get(section, "image_id")
        if self.config.has_option(section, "name"):
            image.name = self.config.get(section, "name")
        if self.config.has_option(section, "desc"):
            image.desc = self.config.get(section, "desc")
        if self.config.has_option(section, 'img'):
            image.img = self.config.get(section, 'img')
        if self.config.has_option(section, 'info'):
            image.info = self.config.get(section, 'info')
        if self.config.has_option(section, "flavor_id"):
            image.flavor_id = self.config.get(section,"flavor_id")
        if self.config.has_option(section, "prefix"):
            image.instance_prefix = self.config.get(section,"prefix")
        if self.config.has_option(section, "check_url"):
            image.instance_check_url = self.config.get(section,"check_url")
        if self.config.has_option(section, "soft_url"):
            image.instance_soft_url = self.config.get(section,"soft_url")
        if self.config.has_option(section, "time"):
            image.instance_time = self.config.get(section,"time")
        if self.config.has_option(section, "max_instance"):
            image.max_instance = self.config.getint(section,"max_instance")
        return image


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
        self.img = None

    def check(self):
        if self.image_id is None:
            raise DemoExceptionInvalidImage('image_id')
        if self.flavor_id is None:
            raise DemoExceptionInvalidImage('flavor_id')
        if self.instance_prefix is None:
            raise DemoExceptionInvalidImage('instance_prefix')
        if self.instance_check_url is None:
            raise DemoExceptionInvalidImage('instance_check_url')
        if self.instance_soft_url is None:
            raise DemoExceptionInvalidImage('instance_soft_url')
        if self.instance_time is None:
            raise DemoExceptionInvalidImage('instance_time')
        if self.max_instance is None:
            raise DemoExceptionInvalidImage('max_instance')
        return True