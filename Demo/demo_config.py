import ConfigParser
import os
from copy import copy
from demo_exception import *

IMAGE_CONF_PREFIX = 'IMAGE_'


class DemoConfig():
    config_file = './config.ini'

    def __init__(self):
        if not os.path.isfile(DemoConfig.config_file):
            raise DemoExceptionConfigNotFound()
        self.config = ConfigParser.ConfigParser()
        self.config.read(DemoConfig.config_file)

        # Default
        self.log_level = self.config.get("DEFAULT", "log_level")
        self.security_type = self.config.get("DEFAULT", "security_type")
        if self.security_type not in ('open', 'email')\
                and not self.security_type.startswith('auth_'):
            raise DemoExceptionBadConfigValue(
                'security_type',
                self.security_type
            )
        self.provider = self.config.get("DEFAULT", "provider")

        # HTTP
        self.http_port = self.config.getint("HTTP", "port")

        # Database
        self.database_connection = self.config.get("DATABASE", "connection")

        # EMAIL CONF
        if self.security_type == 'email':
            self.mail_host = self.config.get("MAIL", "host")
            if self.config.has_option("MAIL", "port"):
                self.mail_port = self.config.getint("MAIL", "port")
            else:
                self.mail_port = 25

            if self.config.has_option("MAIL", "from"):
                self.mail_from = self.config.get("MAIL", "from")
            else:
                self.mail_from = 'demoinstance@localhost'

            if self.config.has_option("MAIL", "user"):
                self.mail_user = self.config.get("MAIL", "user")
            else:
                self.mail_user = None

            if self.config.has_option("MAIL", "password"):
                self.mail_password = self.config.get("MAIL", "password")
            else:
                self.mail_password = None

            if self.config.has_option("MAIL", "tls"):
                self.mail_tls = self.config.getboolean("MAIL", "tls")
            else:
                self.mail_tls = False

        # Auth Conf
        if self.security_type.startswith('auth_'):
            self.auth = {}
            section = self.security_type.upper()
            if self.config.has_section(section):
                for name, value in self.config.items(section):
                    self.auth[name] = value

        # Prov Conf
        self.provider_data = {}
        section = 'PROV_'+self.provider.upper()
        if self.config.has_section(section):
            for name, value in self.config.items(section):
                self.provider_data[name] = value

        # IMAGE CONF
        self.images = {}
        template_image = self.get_image_by_section('IMAGE')
        for section in self.config.sections():
            if not section.startswith(IMAGE_CONF_PREFIX):
                continue
            image = self.get_image_by_section(
                section,
                template_image=template_image
            )
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
            image.flavor_id = self.config.get(section, "flavor_id")
        if self.config.has_option(section, "prefix"):
            image.instance_prefix = self.config.get(section, "prefix")
        if self.config.has_option(section, "check_url"):
            image.instance_check_url = self.config.get(section, "check_url")
        if self.config.has_option(section, "soft_url"):
            image.instance_soft_url = self.config.get(section, "soft_url")
        if self.config.has_option(section, "time_default"):
            image.instance_time = self.config.getint(section, "time_default")
        if self.config.has_option(section, "time_max"):
            image.instance_time_max = self.config.getint(section, "time_max")
        if self.config.has_option(section, "max_instance"):
            image.max_instance = self.config.getint(section, "max_instance")
        if self.config.has_option(section, "user_data"):
            image.user_data = self.config.get(section, "user_data")
        return image


class DemoConfigImage():
    def __init__(self):
        self.image_id = None
        self.flavor_id = None
        self.instance_prefix = None
        self.instance_check_url = None
        self.instance_soft_url = None
        self.instance_time = None
        self.instance_time_max = None
        self.max_instance = None
        self.name = None
        self.desc = None
        self.info = None
        self.img = None
        self.user_data = None

    def check(self):
        if self.image_id is None:
            raise DemoExceptionInvalidImage('image_id')
        if self.flavor_id is None:
            raise DemoExceptionInvalidImage('flavor_id')
        if self.instance_prefix is None:
            raise DemoExceptionInvalidImage('instance_prefix')
        if self.instance_soft_url is None:
            raise DemoExceptionInvalidImage('instance_soft_url')
        if self.instance_time is None:
            raise DemoExceptionInvalidImage('instance_time')
        if self.max_instance is None:
            raise DemoExceptionInvalidImage('max_instance')
        return True
