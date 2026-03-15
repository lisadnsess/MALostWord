# -*- coding: utf-8 -*-
import time
import json
import os
from pathlib import Path

from maa.context import Context
from maa.custom_recognition import CustomRecognition

from utils.logger import logger
from utils.run_task import run_task_param,SuppressOutput

# resource.use_cpu()


# @resource.custom_recognition("EFA_ActionAll")
class EFA_ActionAll(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        print("##########_##########_##########")
        data = json.loads(argv.custom_recognition_param)["fight_json_dir"]
        repeat = int(json.loads(argv.custom_recognition_param)["repeat"])

        parent_dir = Path(__file__).resolve().parent.parent
        json_dir = os.path.join(parent_dir, "FightStrategy", data)
        if not os.path.exists(json_dir):
            json_dir = os.path.join(parent_dir, "FightStrategy", "fight1.json")
            # json_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            #                         os.path.join("FightStrategy", "fight1.json"))
        print(f"json dir: {json_dir}")
        a_json = get_fight_json(json_dir)
        new_ctx = context.clone()

        repeat_number_now = 0
        while repeat_number_now < repeat or repeat < 0:
            start_time_in = time.time()

            repeat_number_now += 1
            print(f"repeat {repeat_number_now}")
            logger.info(f"repeat {repeat_number_now}")
            with SuppressOutput():
                run_task_param(new_ctx, "EF_ActionLine")
            print(f"Start fight")
            with SuppressOutput():
                for fight_one in a_json.values():
                    for screen_one in fight_one.values():
                        run_task_param(new_ctx, "MCA_ActionOneScreen", None, screen_one)
                        run_task_param(new_ctx, "EF_ConnectFight")

            # for fight_one in a_json.values():
            #     # print(fight_one)
            #     for screen_one in fight_one.values():
            #         run_task_param(new_ctx, "MCA_ActionOneScreen", None, screen_one)
            #         run_task_param(new_ctx, "EF_ConnectFight")

            end_time_in = time.time()  # 记录结束时间

            execution_time = end_time_in - start_time_in
            print(f"代码运行时间：{execution_time} 秒")
            logger.info(f"代码运行时间：{execution_time} 秒")
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")

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
    index_fight = 0
    for (fight_key, fight_one) in raw_json.items():
        if not "fight" in fight_key:
            continue
        index_fight += 1
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