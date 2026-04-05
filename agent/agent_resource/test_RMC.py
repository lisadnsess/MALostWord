# -*- coding: utf-8 -*-
import time
import json

from maa.context import Context
from maa.custom_recognition import CustomRecognition

from utils.logger import logger
from utils.run_task import run_task_param, SuppressOutput


class MCR_UseShield(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')

        use_shield = json.loads(argv.custom_recognition_param).get("shield_number")
        logger.debug(f'use_boost:{use_shield}')
        # if not use_shield or use_shield <= 0:
        #     logger.debug(f'use zero shield')
        #     return True
        use_shield = int(use_shield)

        logger.debug(f'use_shield:{use_shield}')


        reco_detail = context.run_recognition("MC_CurrentShield", argv.image)
        current_shield  =len(reco_detail.filtered_results)
        print(current_shield)
        if not reco_detail:
            shield_number = 0
        else:
            shield_number = len(reco_detail.filtered_results)

        bullet_target_number = shield_number + use_shield
        if bullet_target_number >= 5:
            bullet_target_number = 4
        print(bullet_target_number)
        context.run_task(
            "MC_ShieldLine",
            pipeline_override={
                "MC_ShieldLine_1": {"index": int(bullet_target_number)}
            },
        )
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


