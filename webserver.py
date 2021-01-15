#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import functools
import json
import logging
import os
import websockets

from command import (Command, Option)
from game import Game
from player import (Color, Player)

logging.basicConfig()

games = dict()   # code -> game

sockets = dict()   # code -> [(player, websocket), ...]


class DogEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


from http import HTTPStatus


MIME_TYPES = {
    "html": "text/html",
    "js": "text/javascript",
    "css": "text/css"
}


async def process_request(sever_root, path, request_headers):
    """Serves a file when doing a GET request with a valid path."""

    if "Upgrade" in request_headers:
        return  # Probably a WebSocket connection

    path = '/dog.html'

    response_headers = [
        ('Server', 'asyncio websocket server'),
        ('Connection', 'close'),
    ]

    # Derive full system path
    full_path = os.path.realpath(os.path.join(sever_root, path[1:]))

    # Validate the path
    if os.path.commonpath((sever_root, full_path)) != sever_root or \
            not os.path.exists(full_path) or not os.path.isfile(full_path):
        print("HTTP GET {} 404 NOT FOUND".format(path))
        return HTTPStatus.NOT_FOUND, [], b'404 NOT FOUND'

    # Guess file content type
    extension = full_path.split(".")[-1]
    mime_type = MIME_TYPES.get(extension, "application/octet-stream")
    response_headers.append(('Content-Type', mime_type))

    # Read the whole file into memory and send it out
    body = open(full_path, 'rb').read()
    response_headers.append(('Content-Length', str(len(body))))
    print("HTTP GET {} 200 OK".format(path))
    return HTTPStatus.OK, response_headers, body


async def notify(player_sockets):
    if player_sockets:
        await asyncio.wait([websocket.send(json.dumps(player, cls=DogEncoder)) for (player, websocket) in player_sockets])


async def handler(websocket, path):
    player = None
    try:
        player = Player()
        player.options = [
            Option(Command.NEWGAME, None, "Nieuw spel"), 
            Option(Command.JOINGAME, ["#"], "Doe mee met een spel")]
        async for message in websocket:
            option = Option(**json.loads(message))

            if not player.check_option(option):
                await notify([(player, websocket)])
                continue

            if option.command == Command.NEWGAME:
                code = 3936  # random.randint(1000, 9999);
                sockets[code] = [(player, websocket)]
                player.message = f"De andere spelers kunnen meedoen door code {code} in te voeren"
                player.options = []
                await notify(sockets[code])

            elif option.command == Command.JOINGAME:
                code = int(option.args[0])
                socketlist = sockets.get(code)
                if socketlist == None:
                    player.message = f"onbekande code {code}"
                    await notify([(player, websocket)])
                    continue

                sockets[code].append((player, websocket))
                if len(sockets[code]) < 4:
                    player.message = "wacht op de andere spelers"
                    player.options = []
                    await notify([(player, websocket)])

                else:
                    for (player, _) in sockets[code]:
                        player.message = "Kies een kleur om mee te spelen"
                        player.options = [
                            Option(Command.PICKCOLOR, [Color.RED], "Rood"),
                            Option(Command.PICKCOLOR, [Color.BLUE], "Blauw"),
                            Option(Command.PICKCOLOR, [Color.YELLOW], "Geel"),
                            Option(Command.PICKCOLOR, [Color.GREEN], "Groen")
                            ]
                   
                    await notify(sockets[code])

            elif option.command == Command.PICKCOLOR:
                color = option.args[0]
                if any(other.color == color for (other, _) in sockets[code]):
                    player.message = f"Kleur {option.text} is al gekozen door een andere speler. " + player.message
                    await notify([(player, websocket)])
                    continue

                player.color = color
                player.name = option.text
                player.message = "Wacht op de andere spelers"
                player.options = []

                for (other, _) in sockets[code]:
                    other.options = [option for option in other.options if option.args[0] != color]

                if all( not any(p.options) for (p, _) in sockets[code]):
                    game = Game(p for (p, _) in sockets[code])
                    games[code] = game

                await notify(sockets[code])

            else:
                game = games[code]
                game.play_option(player, option)
                await notify(sockets[code])
    finally:
        if player is not None:
            sockets[code].remove((player, websocket))
        pass

if __name__ == "__main__":

    static_handler = functools.partial(process_request, os.path.join(os.getcwd(), 'ui'))

    start_server = websockets.serve(handler, "localhost", 6789, process_request=static_handler)

    print("Running server at http://127.0.0.1:6789/")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
