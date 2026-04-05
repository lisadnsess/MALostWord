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
        logger.debug(f"正在运行节点{argv.node_name}")
        use_shield = json.loads(argv.custom_recognition_param).get("shield_number")
        logger.debug(f"use_shield:{use_shield}")
        if not use_shield or use_shield <= 0:
            logger.debug(f"use zero shield")
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")

        reco_detail = context.run_recognition("MC_CurrentShield", argv.image)
        if not reco_detail:
            shield_number = 0
        else:
            shield_number = len(reco_detail.filtered_results)

        use_shield_number = shield_number + use_shield
        final_shield = 5-use_shield_number
        logger.debug(f"final_shield :{final_shield}")
        if use_shield_number >= 5:
            use_shield_number = 4

        prover = {"MC_ShieldLine_1": {"index": int(use_shield_number)-1}}
        context.override_pipeline(prover)
        context.run_task("MC_ShieldLine")

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


