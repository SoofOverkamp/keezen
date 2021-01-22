#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import functools
import json
import logging
import os
import websockets

from color import Color
from option import OptionCode, Option
from game import Game
from player import ErrorCode, StateCode, Player

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
    player = Player()
    player.options = [
        Option(OptionCode.NEW_GAME, "Nieuw spel"), 
        Option(OptionCode.JOIN_GAME, "Doe mee met een spel", game_code='3936')]
    player.message = "Wat wil je doen?"
    player.set_state(StateCode.START)
    game_code = 0
    try:
        await notify([(player, websocket)])

        async for message in websocket:
            option = Option(**json.loads(message))

            if not player.check_option(option):
                await notify([(player, websocket)])
                continue

            # Thisis a change

            player.set_error(None)

            if option.code == OptionCode.NEW_GAME:
                game_code = 3936  # random.randint(1000, 9999);
                sockets[game_code] = [(player, websocket)]
                player.message = f"De andere spelers kunnen meedoen door code {game_code} in te voeren"
                player.set_state(StateCode.JOIN_OTHERS, game_code=game_code)
                player.options = []
                await notify(sockets[game_code])

            elif option.code == OptionCode.JOIN_GAME:
                game_code = option.game_code
                socketlist = sockets.get(game_code) if game_code > 0 else None
                if socketlist == None:
                    player.message = f"onbekande code {game_code}"
                    player.set_error(ErrorCode.UNKNOWN_CODE, game_code=game_code)
                    await notify([(player, websocket)])
                    continue

                sockets[game_code].append((player, websocket))
                if len(sockets[game_code]) < 4:
                    player.message = "wacht op de andere spelers"
                    player.set_state(StateCode.JOIN_OTHERS, game_code=game_code)
                    player.options = []
                    await notify([(player, websocket)])

                else:
                    for (player, _) in sockets[game_code]:
                        player.message = "Kies een kleur om mee te spelen"
                        player.set_state(StateCode.PICK_COLOR)
                        player.options = [
                            Option(OptionCode.PICK_COLOR, "Rood", color=Color.RED),
                            Option(OptionCode.PICK_COLOR, "Blauw", color=Color.BLUE),
                            Option(OptionCode.PICK_COLOR, "Geel", color=Color.YELLOW),
                            Option(OptionCode.PICK_COLOR, "Groen", color=Color.GREEN)
                            ]
                   
                    await notify(sockets[game_code])

            elif option.code == OptionCode.PICK_COLOR:
                color = option.color
                if any(other.color == color for (other, _) in sockets[game_code]):
                    player.message = f"Kleur {option.text} is al gekozen door een andere speler. " + player.message
                    player.set_error(ErrorCode.COLOR_ALREADY_CHOSEN, color=color) 
                    await notify([(player, websocket)])
                    continue

                player.color = color
                player.name = option.text
                player.message = "Wacht op de andere spelers"
                player.set_state(StateCode.PICK_COLOR_OTHERS)
                player.options = []

                for (other, _) in sockets[game_code]:
                    other.options = [option for option in other.options if option.color != color]

                if all( not any(p.options) for (p, _) in sockets[game_code]):
                    game = Game(p for (p, _) in sockets[game_code])
                    games[game_code] = game

                await notify(sockets[game_code])

            else:
                game = games[game_code]
                game.play_option(player, option)
                await notify(sockets[game_code])
    finally:
        if player is not None and game_code > 0:
            sockets[game_code].remove((player, websocket))
        pass

if __name__ == "__main__":

    static_handler = functools.partial(process_request, os.path.join(os.getcwd(), 'ui'))

    start_server = websockets.serve(handler, "localhost", 6789, process_request=static_handler)

    print("Running server at http://127.0.0.1:6789/")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
