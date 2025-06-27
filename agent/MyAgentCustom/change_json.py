import json
import os

character_one_dict_model = {
    "target": {
        "target_use": False,
        "target_order": 2,
        "target_order_name": ""
    },
    "boost_number": 0,
    "shield_number": 0,
    "target_SpellCard": 0
}

result_model = {
    "auto": False,
    "open_skill1": [],
    "change_character": [],
    "open_skill2": [],
    # "fight": {}
}


def get_fight_json(fight_json_dir_in):
    with open(fight_json_dir_in, encoding="utf-8") as f:
        raw_json = json.load(f)
    new_json = {}
    for index_fight, fight_one in enumerate(raw_json.values()):
        new_json["fight" + str(index_fight)] = {}
        fight_one_dic = new_json["fight" + str(index_fight)]
        pass
        for index_screen, screen_one in enumerate(fight_one):
            # a = result_model
            fight_one_dic["screen" + str(index_screen)] = result_model.copy()
            screen_one_dic = fight_one_dic["screen" + str(index_screen)]
            screen_one_dic["auto"] = screen_one[0]
            screen_one_dic["open_skill1"] = screen_one[1]
            screen_one_dic["change_character"] = screen_one[2]
            screen_one_dic["open_skill2"] = screen_one[3]
            screen_one_dic["fight"] = {}
            character_dic = screen_one_dic["fight"]
            pass
            for index_character, character_one in enumerate(screen_one[4]):
                character_dic["character" + str(index_character)] = character_one_dict_model.copy()
                character_one_dic = character_dic["character" + str(index_character)]
                # "target"
                character_one_dic["target"] = {}
                character_one_dic["target"]["target_use"] = character_one[0][0]
                character_one_dic["target"]["target_order"] = character_one[0][1]
                character_one_dic["target"]["target_order_name"] = character_one[0][2]
                character_one_dic["boost_number"] = character_one[1]
                character_one_dic["shield_number"] = character_one[2]
                character_one_dic["target_SpellCard"] = character_one[3]
                pass

    return new_json


if __name__ == "__main__":

    print(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fight1.json")
    json_dir = "fight1.json"
    a_json = get_fight_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), json_dir))
    for fight_one in a_json.values():
        print(fight_one)
        for screen_one in fight_one.values():
            pass
            for character_one in screen_one.values():
                pass
    a = a_json['fight0']['screen0']

    print()

