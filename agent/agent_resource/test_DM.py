# python -m pip install maafw
import os
import time
import sys

from maa.tasker import Tasker
from maa.toolkit import Toolkit
from maa.context import Context
from maa.resource import Resource
from maa.controller import AdbController
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition
# from maa.agent.agent_server import AgentServer
from maa.notification_handler import NotificationHandler, NotificationType
import json

from utils.logger import logger

# @resource.custom_recognition("DMA_Print")
class DMA_Print(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("DMA_GetDate")
class DMA_GetDate(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
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
        # print("##########_##########_##########")
        logger.info(f"开始每日资源本")
        logger.info(f"今日日常为：{ocr_target}")
        context.override_pipeline({
            "DMA_DailyMaterialAll": {
                "custom_recognition_param": {
                    "current_data": ocr_target}}})

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


# @resource.custom_recognition("DMA_DailyMaterialAll")
class DMA_DailyMaterialAll(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        logger.debug("##########_##########_##########")
        logger.debug(f'正在运行节点{argv.node_name}')
        current_data = json.loads(argv.custom_recognition_param).get("current_data")

        # if current_data is None:
        #     return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")
        if len(current_data) > 0:
            logger.debug(f'当前资源本：{current_data[0]}')
            context.override_pipeline({"DM_DailyMaterialOne": {"expected": current_data.pop(0)}})
            context.override_pipeline({
                "DMA_DailyMaterialAll": {
                    "custom_recognition_param": {
                        "current_data": current_data}}})
            return None
        else:
            logger.debug(f'无可用日常本')
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")

# @resource.custom_recognition("DMA_Logger")
class DMA_Logger(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        info_logger = json.loads(argv.custom_recognition_param).get("info")
        debug_logger = json.loads(argv.custom_recognition_param).get("debug")
        if info_logger:
            logger.info(f'{info_logger}')
        if debug_logger:
            logger.debug(f'{debug_logger}')

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


def merge_json_files_recursive(folder_path):
    """
    递归读取文件夹及其所有子文件夹中的所有JSON文件，
    并将其内容合并为一个字典

    参数:
        folder_path: 根文件夹路径

    返回:
        合并后的字典
    """
    merged_dict = {}
    file_count = 0  # 统计处理的JSON文件数量

    # 递归遍历所有文件夹和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # 检查文件是否为JSON文件
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                file_count += 1

                try:
                    # 打开并读取JSON文件
                    with open(file_path, 'r', encoding='utf-8') as file:
                        json_data = json.load(file)

                        # 确保读取的数据是字典类型
                        if isinstance(json_data, dict):
                            # 将当前JSON文件的内容合并到总字典中
                            # 如果有重复的键，后面的会覆盖前面的
                            merged_dict.update(json_data)
                        else:
                            print(f"警告: {file_path} 中的数据不是字典类型，已跳过")

                except json.JSONDecodeError:
                    print(f"错误: 无法解析 {file_path}，文件可能不是有效的JSON")
                except Exception as e:
                    print(f"处理 {file_path} 时出错: {str(e)}")

    print(f"共处理了 {file_count} 个JSON文件")
    return merged_dict

# if __name__ == "__main__":
#     main()
