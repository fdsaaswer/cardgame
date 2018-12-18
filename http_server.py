#!/usr/bin/python

import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from exception import GameLogicError
from game_server import GameServer

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8892
GAME_SERVER = GameServer()


def serialize(game_server):
    text = '<html><head><title>Game server information</title></head><body>'
    text += '<table border = "1">'
    for player in game_server.players:
        text += '<th>'

        text += '<p>{} {} ({})</p>'.format(
            player.name,
            "*" if player == game_server.players[game_server.active] else "",
            player.health,
        )

        for idx, tile in enumerate(player.tiles):
            text += '<form action="" method="post">'
            text += '<table border = "1">'
            text += '<th>{}</th>'.format(tile.land)
            if tile.unit:
                text += '<th><tr>'
                text += '{}</tr><tr>'.format(tile.unit.name)
                try:
                    if tile.unit.use:
                        text += '<input type="submit" value="{}" name="Use card" />'.format(idx)
                except AttributeError as e:
                    pass
                text += '</tr>'
            else:
                text += '<th>No creature</th>'
            text += '<th>{}</th>'.format(tile.enchantment.name) if tile.enchantment else '<th>No building</th>'
            text += '</table>'

        for idx, card in enumerate(player.hand):
            text += """<form action="" method="post">
                    <input type="submit" value="{}" name="Play card" />{}
                    <input type="text" name="target_id">
                    </form>""".format(idx, card.name)

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
        if post_body:
            post_body = str(post_body)[2:-1].replace('+', ' ').split('&')
            print(post_body)
            params = {param.split('=')[0]: param.split('=')[1] for param in post_body}
            try:
                if params['Play card']:
                    pos_id = int(params['Play card'])
                    target_id = params.get('target_id', None)
                    target_id = int(target_id) if target_id else None
                    GAME_SERVER.play_card(pos_id, target_id)
                if params['Use card']:
                    GAME_SERVER.use_card()
                if params['Draw card']:
                    GAME_SERVER.draw_card()
                if params['End turn']:
                    GAME_SERVER.end_turn()
            except GameLogicError as e:
                self.wfile.write(bytes(str(e), 'UTF-8'))
            except KeyError as e:
                self.wfile.write(bytes('Error:' + str(e), 'UTF-8'))

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