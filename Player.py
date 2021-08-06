

class Player:
    def __init__(self,fpl_player_object,max_price,max_ppg):
        self.player_object = fpl_player_object
        self.pp90 = float(fpl_player_object.pp90)
        self.position = convert_to_pos(fpl_player_object.element_type)
        self.name = fpl_player_object.web_name, 
        self.cost = float(fpl_player_object.now_cost/10)
        self.weight = self.pp90/self.cost


def convert_to_pos(id):
    positions = ["GKP","DEF","MID","FWD"]
    return positions[id-1]
