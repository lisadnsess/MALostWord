# -*- coding: utf-8 -*-
import json

from maa.context import Context
from maa.custom_action import CustomAction

from utils.logger import logger
from utils.run_task import run_task_param


class UF_ActionLogger(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        info_logger = json.loads(argv.custom_action_param).get("info")
        debug_logger = json.loads(argv.custom_action_param).get("debug")

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
        return True


# @resource.custom_action("UF_ActionRunPipeline")
class UF_ActionRunPipeline(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        pipeline_name = json.loads(argv.custom_action_param).get("pipeline_name")
        if pipeline_name:
            if isinstance(pipeline_name, str):
                pipeline_name = [pipeline_name]
            for pipeline_name_one in pipeline_name:
                logger.debug(f'正在运行：{pipeline_name_one}')
                run_task_param(context, pipeline_name_one)
        return True

