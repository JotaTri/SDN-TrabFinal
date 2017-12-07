import tornado.web
import sys

from authenticated import authenticated

import requests

import ast
import json

def create_web_server():
    # Roteamento para as diferentes URIs
    handlers = [
        (r"/token", token),
        (r"/firewall/module/status", firewall_module_status),
        (r"/firewall/module/enable/([0-9]+)", firewall_module_enable),
        (r"/firewall/module/disable/([0-9]+)", firewall_module_disable),
        (r"/firewall/rules/([0-9]+)", firewall_rules),
        (r"/firewall/log/status", firewall_log_status),
        (r"/firewall/log/enable/([0-9]+)", firewall_log_enable),
        (r"/firewall/log/disable/([0-9]+)", firewall_log_disable),
        (r"/firewall/open/module", firewall_open_module),
        (r"/firewall/open/rules/([0-9]+)", firewall_open_rules),
    ]

    # Configuracoes da aplicacao
    settings = dict()

    return tornado.web.Application(handlers, **settings)

class firewall_open_module(tornado.web.RequestHandler):
    def get(self):
        try:
            response = requests.get('http://localhost:8080/firewall/module/status')
        except Exception as e:
            print(str(e))
            return

        self.set_status(200)
        print(type(response))
        print(response)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

class firewall_open_rules(tornado.web.RequestHandler):
    def get(self, switch_id):
        response = requests.get('http://localhost:8080/firewall/rules/' + switch_id)
        self.set_status(response.status_code)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

@authenticated
class firewall_module_status(tornado.web.RequestHandler):
    def get(self):
        try:
            response = requests.get('http://localhost:8080/firewall/module/status')
        except Exception as e:
            print('deu ruim')
            print(str(e))
            return

        self.set_status(200)
        print(type(response))
        print(response)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

@authenticated
class firewall_rules(tornado.web.RequestHandler):
    def get(self, switch_id):
        response = requests.get('http://localhost:8080/firewall/rules/' + switch_id)
        self.set_status(response.status_code)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

    def post(self, switch_id):
        post_data = tornado.escape.json_decode(self.request.body)
        post_data = ast.literal_eval(json.dumps(post_data))
        response = requests.post('http://localhost:8080/firewall/rules/' + switch_id, data=json.dumps(post_data))
        self.set_status(response.status_code)
        try:
            self.write(response.json()[0])
        except Exception as e:
            print('error')
            print(str(e))
            pass
        return

    def delete(self, switch_id):
        post_data = tornado.escape.json_decode(self.request.body)
        response = requests.delete('http://localhost:8080/firewall/rules/' + switch_id, data=json.dumps(post_data))
        self.set_status(response.status_code)
        try:
            self.write(response.json()[0])
        except:
            pass
        return
@authenticated
class firewall_module_enable(tornado.web.RequestHandler):
    def put(self, switch_id):
        nivel_acesso = self.request.headers.get('auth')['user']['nivel_de_acesso']
        if nivel_acesso != 1:
            self.set_status(401)
            self.write({'status':'error', 'message': 'nivel de acesso nao permitido'})
            return
        response = requests.put('http://localhost:8080/firewall/module/enable/' + switch_id)
        self.set_status(response.status_code)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

@authenticated
class firewall_module_disable(tornado.web.RequestHandler):
    def put(self, switch_id):
        nivel_acesso = self.request.headers.get('auth')['user']['nivel_de_acesso']
        if nivel_acesso != 1:
            self.set_status(401)
            self.write({'status':'error', 'message': 'nivel de acesso nao permitido'})
            return

        response = requests.put('http://localhost:8080/firewall/module/disable/' + switch_id)
        self.set_status(response.status_code)
        self.write(response.json()[0])
        return

@authenticated
class firewall_log_enable(tornado.web.RequestHandler):
    def put(self, switch_id):
        response = requests.put('http://localhost:8080/firewall/log/enable/' + switch_id)
        self.set_status(response.status_code)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

@authenticated
class firewall_log_disable(tornado.web.RequestHandler):
    def put(self, switch_id):
        response = requests.put('http://localhost:8080/firewall/log/disable/' + switch_id)

        self.set_status(response.status_code)
        self.write(response.json[0])
        return

@authenticated
class firewall_log_status(tornado.web.RequestHandler):
    def get(self):
        try:
            response = requests.get('http://localhost:8080/firewall/log/status')
        except Exception as e:
            print('deu ruim')
            print(str(e))
            return

        self.set_status(response.status_code)
        print(type(response))
        print(response)
        try:
            self.write(response.json()[0])
        except:
            pass
        return

@authenticated
class token(tornado.web.RequestHandler):
    def get(self):
        usuario = self.request.headers.get('auth')['user']['usuario']
        nivel_acesso = self.request.headers.get('auth')['user']['nivel_de_acesso']

        try:
            coisa = self.get_argument('coisa')
        except:
            self.set_status(400)
            self.write({'status': 'error', 'message': 'missing argument "coisa"'})
            return
        self.set_status(200)
        self.write({'status': 'Ok', 'message': 'Recebido a coisa "' + coisa + '" do usuario: "' + usuario + '" de nivel de acesso: ' + nivel_acesso})
        return


if __name__ == '__main__':
    # Le a porta a ser usada a partir da configuracao lida
    # http_listen_port = ConfigHandler.http_listen_port
    http_listen_port = sys.argv[1]

    web_app = create_web_server()

    ioloop = tornado.ioloop.IOLoop.instance()

    web_app.listen(http_listen_port)
    ioloop.start()
