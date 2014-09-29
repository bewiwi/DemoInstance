from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from Demo.demo_config import DemoConfig
from Demo.demo import Demo
import re
import json
import os
import logging


class Handler(BaseHTTPRequestHandler):

    def send_file(self,file):
        f = open('web/'+file)
        self.send_response(200)
        self.set_mime()
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return

    def instance_create(self):
        id = self.demo.create_instance()
        rep={'id' : id}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(rep))
        self.wfile.write('\n')

        return

    def instance_info(self, instance_id):
        instance = self.demo.get_instance(instance_id)
        if not instance:
            self.send_response(404)
            self.end_headers()
            return

        instance_info = self.demo.get_instance_info(instance)
        info = {'id' : instance_info['id'], 'system_up': False, 'instance_up': False}
        if self.demo.instance_is_up(instance):
            info['instance_up'] = True
            info['id'] = instance_info['id']
            info['address'] = self.demo.get_instance_ip(instance)
            info['demo_address'] = self.demo.get_instance_soft_address(instance)
            info['life_time'] = self.demo.get_instance_life_time(instance)
            if self.demo.check_system_up(instance):
                info['system_up'] = True
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(info))
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
            self.send_header('Content-type', mimetype)

    def do_GET(self):
        str_path = self.path.split('?')[0]
        try:
            self.config = DemoConfig()
            self.demo = Demo(self.config)

            if self.path == "/":
                self.send_file('index.html')
                return

            if os.path.isfile('web/'+str_path):
                self.send_file(str_path)
                return

            if self.path =="/instance/start":
                self.instance_create()
                return

            match = re.match("/instance/(.*)", self.path)
            if match:
                self.instance_info(match.group(1))
                return

            self.send_response(404)

        except Exception as e:
            self.wfile.flush()
            self.send_response(500)
            self.end_headers()
            self.wfile.write(e.message)
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""