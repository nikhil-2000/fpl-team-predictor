import asyncio

import aiohttp
from prettytable import PrettyTable
from Player import Player

from fpl import FPL

import matplotlib.pyplot as plt

class player_object_to_plot:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player

def on_pick(event):
    print(event.player.obj.name)

async def get_players():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()

    return players

def create_plot(players):
    players = remove_low_minutes(players, minutes=90 * 20)
    players = sorted(players, key=lambda x: x.pp90)
    objects = []
    for p in players:
        new = player_object_to_plot(p.pp90, p.selected_by_percent, p)
        objects.append(new)

    fig, ax = plt.subplots()
    for obj in objects:
        player = ax.plot(obj.x, obj.y, 'ro-', picker=0)[0]
        player.obj = obj

    fig.canvas.callbacks.connect('pick_event', on_pick)

    plt.show()


def remove_low_minutes(players, minutes = 200):
    return [player for player in players if player.minutes > minutes]

players = asyncio.run(get_players())
create_plot(players)