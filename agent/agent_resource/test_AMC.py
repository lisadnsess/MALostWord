# -*- coding: utf-8 -*-

import time
import json

from maa.context import Context
from maa.custom_action import CustomAction

from utils.logger import logger
from utils.run_task import run_task_param, SuppressOutput
from pathlib import Path

class MCA_LoadFightStrategy(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        fight_dir_name = json.loads(argv.custom_action_param).get("fight_dir")

        # 当前工作路径
        fight_dir = Path.cwd() / "fight_strategy"/Path(fight_dir_name)
        logger.debug(f'导入战斗策略: {fight_dir_name}')
        with open(fight_dir, "r", encoding="utf-8") as f:
            data = json.load(f)

        for round_index,round_one in data["fight"].items():
            logger.info(f'正在运行:{round_index}')
            print(round_one)
            round_param = {
                "MCA_Round": {"custom_action_param": {"round_param":round_one}}
            }
            context.override_pipeline(round_param)
            context.run_task("MC_Round")
            break

        # # 当前脚本所在文件夹
        # print(Path(__file__).parent)

        return True

class MCA_Round(CustomAction):

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        round_param = json.loads(argv.custom_action_param).get("round_param")
        # return True
        # print(round_param)

        round_param = {'auto_fight': False,
                       'use_skill_1': [],
                       'change_role': False,
                       'change_role_param': [],
                       'use_skill_2': [],
                       'role_action': {
                           '1': {'boost_number': 2, 'change_target': False, 'change_target_param': 2, 'shield_number': 0, 'use_card': True, 'use_card_param': 1},
                           '2': {'boost_number': 2, 'change_target': False, 'change_target_param': 2, 'shield_number': 0, 'use_card': True, 'use_card_param': 1},
                           '3': {'boost_number': 2, 'change_target': False, 'change_target_param': 2, 'shield_number': 0, 'use_card': True, 'use_card_param': 1}},
                       }


        if round_param["auto_fight"] :
            context.run_task("MC_FightAutoOpen")
            time.sleep(2)
            context.run_task("MC_FightAutoClose")
            return True

        context.run_task("MC_FightAutoClose")
        ##########_##########_##########
        # 使用技能
        MCA_UseSkill_param = {
            "MCA_UseSkill": {"custom_action_param": {"use_skill": round_param["use_skill_1"]}}
        }
        context.override_pipeline(MCA_UseSkill_param)
        context.run_task("MC_UseSkill")

        for role_index, role_one in round_param["role_action"].items():
            logger.debug(f'进行第{role_index}位角色操作')
            # 使用灵力强化
            MCA_UseBoost_param = {
                "MCA_UseBoost": {"custom_action_param": {"boost_number": role_one["boost_number"]}}
            }
            context.override_pipeline(MCA_UseBoost_param)
            context.run_task("MC_UseBoost")
            break

        # # 第一位角色
        # role_action
        # role_1_param = round_param.get("role_1")
        #
        # role_2_param = round_param.get("role_2")
        # if role_2_param is not None:
        #
        #
        # role_3_param = round_param.get("role_3")

        ##########_##########_##########
        # 使用技能

        return True

class MCA_UseSkill(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        use_skill = json.loads(argv.custom_action_param).get("use_skill")
        skill_list_box = [
            {"box": [160, 520, 80, 130]},
            {"box": [253, 520, 80, 130]},
            {"box": [345, 520, 80, 130]},
            {"box": [505, 520, 80, 130]},
            {"box": [600, 520, 80, 130]},
            {"box": [693, 520, 80, 130]},
            {"box": [855, 520, 80, 130]},
            {"box": [946, 520, 80, 130]},
            {"box": [1039, 520, 80, 130]},
        ]
        if len(use_skill) == 0:
            logger.debug(f'无需使用技能')
            return True
        logger.debug(f'use_skill:{use_skill}')
        context.run_task("MC_OpenSkillList")
        for index in use_skill:
            target_box = skill_list_box[index - 1]["box"]
            logger.debug(f"使用技能{index}")
            prover = {"MC_UseSkill_2_1": {"roi": target_box},
                      "MC_UseSkill_2_3": {"roi": target_box}
                      }
            context.override_pipeline(prover)
            context.run_task("MC_UseSkill_1")
        context.run_task("MC_CloseSkillList")
        return True

class MCA_UseBoost(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        use_boost = json.loads(argv.custom_action_param).get("boost_number")
        logger.debug(f'use_boost:{use_boost}')
        if use_boost is None or use_boost <= 0:
            logger.debug(f'use zero boost')
            return True
        use_boost = int(use_boost)


        reco_detail = context.run_task("MC_CurrentBoost")
        current_boost = float(reco_detail.nodes[0].recognition.best_result.text)
        final_boost = current_boost - use_boost
        while final_boost < 0:
            final_boost += 1
        final_boost = round(final_boost, 2)

        logger.debug(f"final_boost :{final_boost}")
        prover = {"MC_CurrentBoostFinalFlag": {"expected": str(final_boost)}}
        context.override_pipeline(prover)
        context.run_task("MC_BoostLine")
        return True


