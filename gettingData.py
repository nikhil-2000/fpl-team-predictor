import asyncio

import aiohttp
from prettytable import PrettyTable
from Player import Player

from fpl import FPL

import matplotlib.pyplot as plt

budget = 100

def split_by_position(all_players):
    gks = []
    defs = []
    mids = []
    fwds = []

    for p in all_players:
        if p.position == "GKP": gks.append(p)
        if p.position == "DEF": defs.append(p)
        if p.position == "MID": mids.append(p)
        if p.position == "FWD": fwds.append(p)

    return gks,defs,mids,fwds

def sum_players(players):
    return sum([p.cost for p in players])


def pick_best(players,budget,n_of_players):
    idx = 0
    current_players = players[idx:idx+n_of_players]
    current_budget = sum_players(current_players)
    while current_budget > budget:

        idx += 1
        current_players = players[idx:idx+n_of_players]
        current_budget = sum_players(current_players)

    return current_players

def output_team(team):
    for pos in team:
        names = [p.name for p in pos]
        print(names, sum_players(pos))

    cost = sum([sum_players(players) for players in team])
    print(cost)

def create_team(all_players, budget_split = [6,16,40,21] ):
    '''
    Choose a starting squad using weight
    Improve squad with best pp90 players within the budget
    '''
    goalkeepers,defenders,midfielders,forwards = split_by_position(all_players)
    all_by_position = [goalkeepers,defenders,midfielders,forwards]
    no_of_pos = [1,3,5,2]
    team = []
    for i in range(4):
        players = all_by_position[i]
        budget = budget_split[i]
        players_to_pick = no_of_pos[i]
        picked = pick_best(players,budget,players_to_pick)
        team.append(picked)

    output_team(team)


positions = ["GKP","DEF","MID","FWD"]
colours = ["Blue","Green","Red","Yellow"]

def convert_to_pos(id):
    return positions[id-1]

def convert_to_id(pos):
    return colours[positions.index(pos)]

def plot_price_pp90(all_players):
    xs = []
    ys = []
    for p in all_players:
        xs.append(p.cost)
        ys.append(p.pp90)

    plt.xticks([i*5 for i in range(13)])
    plt.legend()
    plt.scatter(ys,xs, c = [convert_to_id(p.position) for p in all_players])
    plt.show()

def remove_low_minutes(players, minutes = 200):
    return [player for player in players if player.player_object.minutes > minutes]

async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()

    top_performers = sorted(
        players, key=lambda x: x.points_per_game, reverse=True)
    max_price = float(max(players, key=lambda x: x.now_cost).now_cost)
    max_pp90 = float(top_performers[0].pp90)
    all_players = remove_low_minutes([Player(player_object,max_price,max_pp90) for player_object in top_performers],11*45)
    all_players = sorted(all_players, key=lambda x:x.weight, reverse=True)

    player_table = PrettyTable()
    player_table.field_names = ["Player","Pos", "£","PPG","Weight"]

    for player in all_players[:50]:
        player_table.add_row([player.name,player.position, f"£{player.cost}", player.pp90,player.weight])

    print(player_table)
    # plot_price_pp90(all_players)
    create_team(all_players)

if __name__ == "__main__":
    asyncio.run(main())
