#!/usr/bin/python

import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from game_server import GameServer

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8908
GAME_SERVER = GameServer()


def serialize(game_server):
    text = '<html><head><title>Game server information</title></head><body>'
    text += '<table>'
    for player in game_server.players:
        text += '<th>'
        text += '<p>{} {} ({})</p>'.format(
            player.name,
            "*" if player == game_server.players[game_server.active] else "",
            player.health,
        )
        for tile in player.tiles:
            if tile.unit:
                text += """<form action="" method="post">
                        <input type="submit" value="{}" name="Use card" />
                        </form>""".format(tile.unit.name)
            else:
                text += """<form>Empty slot</form>"""
        for card in player.hand:
            text += """<form action="" method="post">
                    <input type="submit" value="{}" name="Play card" />
                    </form>""".format(card.name)
        text += """<form action="" method="post">
                <input type="submit" value="Draw card" name="Draw card" />
                </form>"""
        text += """<form action="" method="post">
                <input type="submit" value="End turn" name="End turn" />
                </form>"""
        text += '</th>'
    text += '/<table>'
    text += '</body></html>'
    return text


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