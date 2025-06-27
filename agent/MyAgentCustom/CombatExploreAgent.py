# -*- coding: utf-8 -*-
from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.custom_action import CustomAction
from maa.context import Context
from maa.toolkit import Toolkit

import time

@AgentServer.custom_recognition("CEA_GetDailyTime")
class CEA_GetDailyTime(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        """
        根据日选择对应日常位置
        :param context:
        :param argv:node_name
                    custom_recognition_name
                    custom_recognition_param
                    image
                    roi
        :return:
        """
        time_now = time.strftime('%A', time.localtime())
        ocr_target_dic = {
            "Monday": "寻找指南书",
            "Tuesday": "寻找华片",
            "Wednesday": "寻找卷轴",
            "Thursday": "寻找指南书",
            "Friday": "寻找华片",
            "Saturday": "寻找卷轴",
            "Sunday": ["寻找指南书", "寻找华片", "寻找卷轴"],
        }
        ocr_target = ocr_target_dic[time_now]
        print(ocr_target)
        #下滑保证三个日常都在框内
        swipe_job = context.tasker.controller.post_swipe(850, 560,850,120,200)
        swipe_job.wait()

        reco_detail = context.run_recognition(
            "CEA_OCR",
            argv.image,
            pipeline_override={"CEA_OCR": {"recognition": "OCR","roi": [572, 63, 649, 544], "expected": ocr_target}},
        )
        # print(reco_detail)
        if reco_detail is not None:
            print(reco_detail.best_result)
            print(reco_detail.box)
        # print("MyCustomRecognition is running!")
            return CustomRecognition.AnalyzeResult(
                box=reco_detail.box, detail=ocr_target
            )
        return CustomRecognition.AnalyzeResult(
            box=None, detail="无目标"
        )