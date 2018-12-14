#!/usr/bin/python

import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from game_server import GameServer

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8893
GAME_SERVER = GameServer()


def serialize(game_server):
    text = '<html><head><title>Game server information</title></head><body>'
    for player in game_server.players:
        text += '<p>{}</p>'.format(player.health)
    text += """<form action="" method="post">
            <input type="submit" name="upvote" value="Upvote" />
            </form>"""
    text += '</body></html>'
    return text


class Handler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(bytes(serialize(GAME_SERVER), 'UTF-8'))

    def do_POST(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(bytes('test', 'UTF-8'))
        s.wfile.write(bytes(serialize(GAME_SERVER), 'UTF-8'))

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), Handler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))