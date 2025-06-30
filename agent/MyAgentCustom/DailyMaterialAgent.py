# -*- coding: utf-8 -*-
import time

from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from utils import logger
from .GeneralAgent import run_task_param


@AgentServer.custom_recognition("DMA_ActionDailyMaterial")
class DMA_ActionDailyMaterial(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        time_now = time.strftime('%A', time.localtime())
        ocr_target_dic = {
            "Monday": ["寻找指南书"],
            "Tuesday": ["寻找华片"],
            "Wednesday": ["寻找卷轴"],
            "Thursday": ["寻找指南书"],
            "Friday": ["寻找华片"],
            "Saturday": ["寻找卷轴"],
            "Sunday": ["寻找指南书", "寻找华片", "寻找卷轴"],
        }
        ocr_target = ocr_target_dic[time_now]
        print("##########_##########_##########")
        logger.info(f"开始每日资源本")
        new_ctx = context.clone()
        run_task_param(new_ctx, "BL_ActionStart")
        run_task_param(new_ctx, "DM_JoinInExplore")
        time.sleep(0.5)
        context.tasker.controller.post_swipe(850, 560, 850, 120, 200).wait()
        time.sleep(0.5)
        for ocr_target_one in ocr_target:
            logger.info(f"进入资源本：{ocr_target_one}")
            new_ctx.override_pipeline({"DM_DailyMaterialOpenClick": {"expected": ocr_target_one}})
            run_task_param(new_ctx, "DM_DailyMaterialOpen")
            daily_number = run_task_param(
                new_ctx, "DM_IfDailyMaterialFinish").nodes[0].recognition.filterd_results[0].text
            if "0" in daily_number:
                run_task_param(new_ctx, "BL_ReturnOne")
                continue
            run_task_param(new_ctx, "DM_DailyMaterialSwipeDown")
            run_task_param(new_ctx, "AC_FightReplayRepeat")
        logger.info(f"finish DailyMaterial")

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")