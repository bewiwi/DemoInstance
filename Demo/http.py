from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from Demo.demo_config import DemoConfig
from Demo.demo import Demo
from Demo.demo_exception import DemoExceptionToMuchInstance
import re
import json
import os
import logging
import Cookie

COOKIE_SESSION_NAME = 'token'


class Handler(BaseHTTPRequestHandler, object):
    def __init__(self, *args, **kwargs):
        self.config = DemoConfig()
        self.demo = Demo(self.config)
        self.user = None
        self.headers_to_send = {}
        super(Handler, self).__init__(*args, **kwargs)

    def send_error(self,code,message):
        self.wfile.flush()
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}))

    def send_all_header(self, code=200):
        self.send_response(code)
        logging.debug('Add Header')
        for name, value in self.headers_to_send.items():
            logging.debug('name %s value %s', name, value)
            self.send_header(name, value)
        self.end_headers()

    def send_file(self,file):
        f = open('web/'+file)
        self.set_mime()
        self.send_all_header(200)
        self.wfile.write(f.read())
        f.close()
        return

    def instance_create(self,image_key, time=None):
        id = self.demo.create_instance(image_key, token=self.user.token, time=time)
        rep={'id': id}
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(201)
        self.wfile.write(json.dumps(rep))
        self.wfile.write('\n')
        return

    def instance_info(self, instance_id):
        instance = self.demo.get_instance(instance_id)
        if not instance:
            self.send_error(404, 'No instance found')
            return

        instance_info = self.demo.get_instance_info(instance)
        info = {'id': instance_info['id'], 'system_up': False, 'instance_up': False}
        if self.demo.instance_is_up(instance):
            info['instance_up'] = True
            info['id'] = instance_info['id']
            info['address'] = self.demo.get_instance_ip(instance)
            info['demo_address'] = self.demo.get_instance_soft_address(instance)
            info['life_time'] = self.demo.get_instance_life_time(instance)
            if self.demo.check_system_up(instance):
                info['system_up'] = True
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(info))
        return

    def images_info(self):
        http_images = {}
        for name in self.config.images.keys():
            image = self.config.images[name]
            data = {
                'name': image.name,
                'desc': image.desc,
                'img': image.img,
                'max_time': image.instance_time_max,
                'default_time': image.instance_time
            }
            http_images[name] = data
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(http_images))
        return

    def image_info(self, image_key):
        http_images = {}
        if not self.config.images.has_key(image_key):
            self.send_error(404,'Image not found')
            return
        image = self.config.images[image_key]
        data = {
            'name': image.name,
            'desc': image.desc,
            'img': image.img,
            'max_time': image.instance_time_max,
            'default_time': image.instance_time,
            'info': image.info
        }
        http_image = data
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(http_image))
        return

    def set_mime(self):
        mimetype = None
        if self.path.endswith(".html"):
            mimetype='text/html'
        if self.path.endswith(".js"):
            mimetype='application/javascript'
        if self.path.endswith(".css"):
            mimetype='text/css'
        if self.path.endswith(".jpg"):
            mimetype='image/jpg'
        if self.path.endswith(".gif"):
            mimetype='image/gif'
        if self.path.endswith(".png"):
            mimetype='image/png'
        if mimetype is not None:
            self.headers_to_send['Content-type'] = mimetype

    def do_GET(self):
        str_path = self.path.split('?')[0]
        try:
            self.cookie_session()
            if self.path == "/":
                self.send_file('index.html')
                return

            if os.path.isfile('web/'+str_path):
                self.send_file(str_path)
                return

            if self.path =="/image":
                self.images_info()
                return

            match = re.match("/instance/(.*)", self.path)
            if match:
                self.instance_info(match.group(1))
                return

            match = re.match("/image/(.*)", self.path)
            if match:
                self.image_info(match.group(1))
                return

            self.send_error(404, 'No action')

        except DemoExceptionToMuchInstance as e:
            self.send_error(500, e.message)
        return

    def do_PUT(self):
        try:
            self.cookie_session()
            length = int(self.headers.getheader('Content-Length'))
            put_vars = json.loads(self.rfile.read(length))

            match = re.match("/instance/(.*)", self.path)
            if match:
                time = None
                if put_vars.has_key('time'):
                    time = int(put_vars['time'])
                self.instance_create(match.group(1), time=time)
                return
            self.send_error(404, 'No action')
        except DemoExceptionToMuchInstance as e:
            self.send_error(400, e.message)
        except Exception as e:
            self.send_error(500, e.message)
        return

    def cookie_session(self):
        token = self.read_cookie(COOKIE_SESSION_NAME)
        if token is not None:
            self.user = self.demo.get_user_by_token(token)
            if self.user:
                return
        logging.debug('New User')
        self.user = self.demo.create_user()
        self.write_cookie(COOKIE_SESSION_NAME, self.user.token)

    def write_cookie(self, name, value):
        c = Cookie.SimpleCookie()
        c[name] = value
        c[name]['max-age'] = 999999999999999999 #It must be ok :D
        logging.debug('New cookie : %s %s', name, value)
        self.headers_to_send['Set-Cookie'] = c.output(header='')

    def read_cookie(self, name):
        if "Cookie" in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])
            logging.debug(" Cookies : %s", self.headers["Cookie"])
            if not name in c:
                return None
            return c[name].value
        return None


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""