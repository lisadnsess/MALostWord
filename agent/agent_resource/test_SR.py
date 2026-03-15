# python -m pip install maafw
import os
import time
import sys
from pathlib import Path
import json

from maa.context import Context
from maa.custom_recognition import CustomRecognition

from utils.logger import logger
from utils.run_task import run_task_param, SuppressOutput


# @resource.custom_recognition("SRA_ActionSpiritRevival")
class SRA_ActionSpiritRevival(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        """

        1.进入战斗
        :param argv:
        :return:
        """
        new_ctx = context.clone()
        # from MyAgentCustom.change_json import get_fight_json
        logger.info(f"##########_##########_##########")
        logger.info(f"开始复灵首通")
        # logger.debug(f"开始复灵首通")
        data_name = json.loads(argv.custom_recognition_param)["fight_json_dir"]
        # repeat = int(json.loads(argv.custom_recognition_param)["repeat"])

        parent_dir = Path(__file__).resolve().parent.parent
        json_dir = os.path.join(parent_dir, "FightStrategy", data_name)
        logger.debug(f"{json_dir}")
        if not os.path.exists(json_dir):
            json_dir = os.path.join(parent_dir, "FightStrategy", "fight1.json")
        logger.debug(f"{json_dir}")
        a_json = get_fight_json(json_dir)
        json_fight = {k: v for k, v in a_json.items() if "fight" in k}
        try:
            json_debuff = a_json["debuff"]
        except:
            json_debuff = {}
        for screen_one in json_fight["fight1"].values():
            # logger.debug(f"start")
            run_task_param(context, "MCA_ActionOneScreen", None, screen_one)
            # run_task_param(new_ctx, "EF_ConnectFight")
        # run_task_param(new_ctx, "MCA_ActionOneScreen", None, json_fight["fight0"])
        # run_task_param(new_ctx, "EF_ConnectFight")

        # new_ctx = context.clone()
        # run_task_param(new_ctx, "BL_ActionStart")
        # run_task_param(new_ctx, "DM_JoinInExplore")
        # time.sleep(0.5)
        # context.tasker.controller.post_swipe(850, 560, 850, 120, 200).wait()
        # time.sleep(0.5)
        # for ocr_target_one in ocr_target:
        #     logger.info(f"进入资源本：{ocr_target_one}")
        #     new_ctx.override_pipeline({"DM_DailyMaterialOpenClick": {"expected": ocr_target_one}})
        #     run_task_param(new_ctx, "DM_DailyMaterialOpen")
        #     daily_number = run_task_param(
        #         new_ctx, "DM_IfDailyMaterialFinish").nodes[0].recognition.filterd_results[0].text
        #     if "0" in daily_number:
        #         run_task_param(new_ctx, "BL_ReturnOne")
        #         continue
        #     run_task_param(new_ctx, "DM_DailyMaterialSwipeDown")
        #     run_task_param(new_ctx, "AC_FightReplayRepeat")
        # logger.info(f"finish DailyMaterial")
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


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
            fight_one_dic["screen" + str(index_screen)] = {}
            screen_one_dic = fight_one_dic["screen" + str(index_screen)]
            screen_one_dic["auto"] = screen_one[0]
            screen_one_dic["open_skill1"] = screen_one[1]
            screen_one_dic["change_character"] = screen_one[2]
            screen_one_dic["open_skill2"] = screen_one[3]
            screen_one_dic["fight"] = {}
            character_dic = screen_one_dic["fight"]
            pass
            for index_character, character_one in enumerate(screen_one[4]):
                character_dic["character" + str(index_character)] = {}
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
