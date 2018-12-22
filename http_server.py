#!/usr/bin/python

import time
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

from exception import GameLogicError
from game_server import GameServer

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8906
GAME_SERVER = GameServer()


def serialize(game_server):
    return game_server.to_html()


class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(serialize(GAME_SERVER), 'UTF-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.wfile.write(post_body)
        if post_body:
            post_body = str(post_body)[2:-1].replace('+', ' ').split('&')
            print(post_body)
            params = {param.split('=')[0]: param.split('=')[1] for param in post_body}
            try:
                if params.get('Play card', None):
                    pos_id = int(params['Play card'])
                    target_id = params.get('target_id', None)
                    target_id = int(target_id) if target_id else None
                    GAME_SERVER.play_card(pos_id, target_id)
                if params.get('Use card', None):
                    GAME_SERVER.use_card()
                if params.get('Draw card', None):
                    GAME_SERVER.draw_card()
                if params.get('End turn', None):
                    GAME_SERVER.end_turn()
            except GameLogicError as e:
                self.wfile.write(bytes(str(e), 'UTF-8'))
            except Exception as e:
                traceback.print_exc(e)
                self.wfile.write(bytes('Unexpected exception:' + str(e), 'UTF-8'))

        self.wfile.write(bytes(serialize(GAME_SERVER), 'UTF-8'))

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), Handler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))