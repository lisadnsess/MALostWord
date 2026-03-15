# python -m pip install maafw
import os
import time
import sys

from maa.context import Context

from maa.custom_recognition import CustomRecognition
import json

from utils.logger import logger


class DMA_Print(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")






# if __name__ == "__main__":
#     main()
