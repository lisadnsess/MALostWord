# -*- coding: utf-8 -*-
import os
import time
import json
from pathlib import Path
from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context

from .change_json import get_fight_json
from .GeneralAgent import run_task_param, SuppressOutput
from utils import logger

@AgentServer.custom_recognition("EFA_ActionAll")
class EFA_ActionAll(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        print("##########_##########_##########")
        data = json.loads(argv.custom_recognition_param)["fight_json_dir"]
        repeat = int(json.loads(argv.custom_recognition_param)["repeat"])

        parent_dir  = Path(__file__).resolve().parent.parent
        json_dir = os.path.join(parent_dir, "FightStrategy", data)
        if not os.path.exists(json_dir):
            json_dir = os.path.join(parent_dir, "FightStrategy", "fight1.json")
        logger.info(f"进行战斗：{json_dir}")
        a_json = get_fight_json(json_dir)
        new_ctx = context.clone()

        repeat_number_now = 0
        while repeat_number_now < repeat or repeat < 0:
            start_time_in = time.time()

            repeat_number_now += 1
            logger.info(f"正在进行第{repeat_number_now}次循环")
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
            logger.info(f"战斗时间：{execution_time} 秒")
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")
