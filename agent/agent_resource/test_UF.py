# python -m pip install maafw
import os
import time
import sys
import json

from maa.context import Context
from maa.custom_recognition import CustomRecognition

from utils.logger import logger
from utils.run_task import run_task_param


# @resource.custom_recognition("UF_RecognitionCustom")
class UF_RecognitionCustom(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        import copy
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        new_ctx = context.clone()
        recognition_action = copy.deepcopy(json.loads(argv.custom_recognition_param).get("recognition_action"))
        recognition_flag = copy.deepcopy(recognition_action)
        recognition_operate = copy.deepcopy(recognition_action)
        recognition_flag_base = json.loads(argv.custom_recognition_param).get("recognition_flag")
        recognition_operate_base = json.loads(argv.custom_recognition_param).get("recognition_operate")

        recognition_flag.update(recognition_flag_base)
        recognition_operate.update(recognition_operate_base)
        # logger.warning(f'{recognition_action}')
        # logger.warning(f'{recognition_flag}')
        # logger.warning(f'{recognition_operate}')
        if not recognition_action:
            logger.warning(f'{argv.node_name}节点无有效识别信息，跳过该节点')
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="error")

        new_ctx.override_pipeline({"UF_ActionFlag": recognition_flag})
        new_ctx.override_pipeline({"UF_ActionOperate": recognition_operate})
        new_ctx.override_pipeline({"UF_ActionOperate": recognition_action})

        run_task_param(new_ctx, "UF_Action")
        del new_ctx
        # # return None
        logger.debug(f'节点{argv.node_name}已完成运行')
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("UF_CountClean")
class UF_CountClean(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        clean_node_name = json.loads(argv.custom_recognition_param).get("clean_node_name")
        target_number = json.loads(argv.custom_recognition_param).get("target_number")
        if not target_number or target_number == "set_in_code" or type(target_number) == str:
            logger.warning(f'{argv.node_name}节点无目标循环次数，设置为默认值5')
            target_number = 5
        if not clean_node_name or clean_node_name == "UF_Count":
            logger.warning(f'{argv.node_name}节点无清除对象，暂不进行清除操作')
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")

        context.override_pipeline({
            clean_node_name: {
                "custom_recognition_param": {
                    "current_number": 0,
                    "target_number": target_number

                }}})
        logger.debug(f'已将节点{clean_node_name}计数清零，循环次数设置为{target_number}')
        logger.debug(f'节点{argv.node_name}已完成运行')
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("UF_Count")
class UF_Count(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        current_number = json.loads(argv.custom_recognition_param).get("current_number")
        target_number = json.loads(argv.custom_recognition_param).get("target_number")
        if not target_number or type(target_number) == str:
            logger.warning(f'{argv.node_name}节点无目标循环次数')
            return None
        target_number = int(target_number)
        if type(target_number) != int:
            logger.warning(f'{argv.node_name}节点无目标循环次数')
            return None
        if target_number < 0:
            logger.debug(f'运行次数为{str(current_number + 1)}，目标次数为无限')
            context.override_pipeline({
                argv.node_name: {
                    "custom_recognition_param": {
                        "current_number": current_number + 1,
                        "target_number": target_number
                    }}})
            return None
        if current_number < target_number:
            logger.debug(f'运行次数为{str(current_number + 1)}，目标次数为{target_number}')
            context.override_pipeline({
                argv.node_name: {
                    "custom_recognition_param": {
                        "current_number": current_number + 1,
                        "target_number": target_number
                    }}})
            return None
        else:
            logger.debug(f'已达到循环上限，循环终止，目标循环次数为{str(current_number)}')
            logger.debug(f'节点{argv.node_name}已完成运行')
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("UF_Logger")
class UF_Logger(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        info_logger = json.loads(argv.custom_recognition_param).get("info")
        debug_logger = json.loads(argv.custom_recognition_param).get("debug")

        if info_logger:
            if isinstance(info_logger, str):
                info_logger = [info_logger]
            for info_one in info_logger:
                logger.info(f'{info_one}')
        if debug_logger:
            if isinstance(debug_logger, str):
                debug_logger = [debug_logger]
            for debug_one in debug_logger:
                logger.debug(f'{debug_one}')
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("UF_ChangePipeline")
class UF_ChangePipeline(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        target_pipeline = json.loads(argv.custom_recognition_param).get("target_pipeline")
        change_str = json.loads(argv.custom_recognition_param).get("change_str")
        context.override_pipeline({target_pipeline: change_str})
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("UF_RunPipeline")
class UF_RunPipeline(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        pipeline_name = json.loads(argv.custom_recognition_param).get("pipeline_name")
        if pipeline_name:
            if isinstance(pipeline_name, str):
                pipeline_name = [pipeline_name]
            for pipeline_name_one in pipeline_name:
                logger.debug(f'正在运行：{pipeline_name_one}')
                run_task_param(context, pipeline_name_one)
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")
