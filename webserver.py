#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import functools
import json
import logging
import os
import random
import websockets
from http import HTTPStatus


from color import Color
from option import OptionCode, Option
from game import Game
from player import ErrorCode, StateCode, Player

logging.basicConfig()

games = dict()   # code -> game

sockets = dict()   # code -> [(player, websocket), ...]

users = ["Anna", "Bob", "Cynthia", "Daan", "Esther", "Frank", "Gerben", "Hanna", "Ida", "Joost", "Karin", "Loes", "Max", "Nina"]


class DogEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


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
    player = Player(name=users[0])
    player.options = [
        Option(OptionCode.NEW_GAME, "Nieuw spel"), 
        Option(OptionCode.JOIN_GAME, "Doe mee met een spel", game_code='3936')]
    player.message = "Wat wil je doen?"
    player.state = StateCode.START
    game_code = 0
    game = None
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
                game = Game()
                games[game_code] = game
                if option.user_name is None:
                    option.user_name = users[0]
                    users.append(users[0])
                    users.remove(users[0])
                player = game.join_player(option.user_name)
                sockets[game_code] = [(player, websocket)]
                await notify(sockets[game_code])

            elif option.code == OptionCode.JOIN_GAME:
                game_code = option.game_code
                game = games.get(game_code) if game_code > 0 else None

                if game is None:
                    player.message = f"onbekande code {game_code}"
                    player.set_error(ErrorCode.UNKNOWN_CODE, game_code=game_code)
                    await notify([(player, websocket)])
                    continue

                if option.user_name is None:
                    option.user_name = users[0]
                    users.append(users[0])
                    users.remove(users[0])
                player = game.join_player(option.user_name)
                sockets[game_code].append((player, websocket))
                await notify(sockets[game_code])

            else:
                game = games[game_code]
                game.play_option(player, option)
                await notify(sockets[game_code])
    finally:
        if player is not None:
            if game is not None:
                game.unjoin_player(player)

            if game_code > 0:
                sockets[game_code].remove((player, websocket))
                await notify(sockets[game_code])


if __name__ == "__main__":

    random.seed()

    static_handler = functools.partial(process_request, os.path.join(os.getcwd(), 'ui'))

    start_server = websockets.serve(handler, "localhost", 6789, process_request=static_handler)

    print("Running server at http://127.0.0.1:6789/")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
