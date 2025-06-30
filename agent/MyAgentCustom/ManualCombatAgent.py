# -*- coding: utf-8 -*-
import time

from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
import json
from .GeneralAgent import run_task_param
from utils import logger

@AgentServer.custom_recognition("MCA_ActionOneScreen")
class MCA_ActionOneScreen(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        print("##########_##########_##########")
        data = json.loads(argv.custom_recognition_param)
        new_ctx = context.clone()
        print(data)
        if data["auto"]:
            print("use auto")
            logger.info("本面使用自动战斗")
            run_task_param(new_ctx, "MC_FightAutoOpen")
            time.sleep(0.5)
            run_task_param(new_ctx, "MC_FightAutoClose")
            time.sleep(0.5)
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")
        if data["open_skill1"]:
            run_task_param(new_ctx, "MCA_ActionSkillOpen", "open_skill", data["open_skill1"])
            time.sleep(0.5)
        if data["change_character"]:
            print("run change")
            run_task_param(new_ctx, "MCA_ActionChangeCharacter", "change_character", data["change_character"])
            time.sleep(0.5)
            if data["open_skill2"]:        
                run_task_param(new_ctx, "MCA_ActionSkillOpen", "open_skill", data["open_skill2"])
                time.sleep(0.5)
        for index,data_one in enumerate(data["fight"].values()):
            print(data_one["target"])
            if data_one["target"]["target_use"]:
                run_task_param(new_ctx, "MCA_ActionChooseTarget", data_one, data_one["target"])
                time.sleep(0.5)
            run_task_param(new_ctx, "MCA_ActionBoost", "boost_number", data_one["boost_number"])
            time.sleep(0.5)
            run_task_param(new_ctx, "MCA_ActionShield", "shield_number", data_one["shield_number"])
            time.sleep(0.5)
            run_task_param(new_ctx, "MCA_ActionSpellCardUse", "target_SpellCard", data_one["target_SpellCard"])
            time.sleep(0.5)
            if (index == len(data["fight"].values()) - 1):
                time.sleep(5)
                run_task_param(context, "MCA_SpellCardClickOneFlag")
                continue
            run_task_param(context, "MCA_SpellCardFinishFlag")

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


@AgentServer.custom_recognition("MCA_ActionSkillOpen")
class MCA_ActionSkillOpen(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        print("##########_##########_##########")
        open_skill_choose = json.loads(argv.custom_recognition_param)["open_skill"]
        logger.info(f"使用技能:{open_skill_choose}")
        print(open_skill_choose)
        skill_list_box = [
            {"box": [162, 623, 75, 23]},
            {"box": [255, 623, 76, 23]},
            {"box": [348, 623, 75, 23]},
            {"box": [511, 623, 74, 22]},
            {"box": [601, 623, 76, 23]},
            {"box": [695, 623, 75, 23]},
            {"box": [855, 621, 76, 26]},
            {"box": [946, 623, 79, 22]},
            {"box": [1039, 623, 77, 23]}
        ]
        MCA_SkillOpen_roi = list(argv.roi)
        context.run_task("MC_OpenSkillList")
        ########################################
        # reco_detail = context.run_task(
        #     "MCA_SkillOpen_OCR",
        #     pipeline_override={
        #         "MCA_SkillOpen_OCR": {"recognition": "OCR", "roi": MCA_SkillOpen_roi, "expected": ["等级"]}
        #     },
        # )
        ########################################
        # print(reco_detail.nodes[0].recognition.filterd_results)
        for index in open_skill_choose:
            ########################################
            # target_box = reco_detail.nodes[0].recognition.filterd_results[index - 1].box
            target_box = skill_list_box[index - 1]["box"]
            ########################################
            roi_one = [target_box[0], MCA_SkillOpen_roi[1], target_box[2], MCA_SkillOpen_roi[3]]
            print(f"click {index} skill, roi = {roi_one}")
            ppover = {"MCA_SkillOpenFinishFlag": {"roi": roi_one},
                      "MCA_SkillOpenClick": {"roi": roi_one}
                      }
            context.override_pipeline(ppover)
            context.run_task("MCA_SkillOpenOne")
        context.run_task("MC_CloseSkillList")
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="完成技能")


@AgentServer.custom_recognition("MCA_ActionChangeCharacter")
class MCA_ActionChangeCharacter(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        print("##########_##########_##########")
        change_character = json.loads(argv.custom_recognition_param)["change_character"]
        # logger.info(f"交换人物{change_character}")
        current_character = run_task_param(context, "MCA_CurrentCharacter").nodes[0].recognition.filterd_results[0].text
        roi = [1094, 48, 54, 45]
        if current_character == "2" or current_character == "3":
            context.tasker.controller.post_click(70, 670).wait()
            time.sleep(0.5)
            context.tasker.controller.post_click(70, 670).wait()
            time.sleep(0.5)
        current_character = int(
            run_task_param(context, "MCA_CurrentCharacter").nodes[0].recognition.filterd_results[0].text)

        new_ctx = context.clone()

        for index in range(3):
            if current_character in change_character:
                # print(f"交换{current_character}位角色")
                logger.info(f"交换{current_character}位角色")
                context.tasker.controller.post_click(int(roi[0] + roi[2] / 2), int(roi[1] + roi[3] / 2)).wait()
                time.sleep(2)
                current_character = \
                    int(run_task_param(context, "MCA_CurrentCharacter").nodes[0].recognition.filterd_results[0].text)
            if index < 2:
                context.tasker.controller.post_click(320, 580).wait()
                current_character += 1
                run_task_param(new_ctx, "MCA_CurrentCharacter",
                               pipeline_override_data={"expected": [str(current_character)]})

        run_task_param(context, "MCA_ReturnOneCharacter")

        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")

@AgentServer.custom_recognition("MCA_ActionBoost")
class MCA_ActionBoost(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        print("##########_##########_##########")
        use_boost = int(json.loads(argv.custom_recognition_param)["boost_number"])
        # print(f"use_boost is {use_boost}")
        logger.info(f"use_boost is {use_boost}")
        if not use_boost or use_boost <= 0:
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="不使用灵力")
        reco_detail = context.run_task("MCA_CurrentBoostFlag")
        current_boost = float(reco_detail.nodes[0].recognition.filterd_results[0].text)
        # print(f"current_boost is {current_boost}")
        logger.info(f"current_boost is {current_boost}")
        final_boost = current_boost - use_boost
        while final_boost < 0:
            final_boost += 1
        final_boost = round(final_boost, 2)
        # print(f"final_boost is {final_boost}")
        logger.info(f"final_boost is {final_boost}")

        ########################################
        # click_number = round(current_boost - final_boost)
        # roi = [1003, 547, 133, 50]
        # for _ in range(click_number):
        #     context.tasker.controller.post_click(
        #         int(roi[0] + roi[2] / 2), int(roi[1] + roi[3] / 2)
        #     ).wait()
        #     time.sleep(0.5)
        context.run_task(
            "MCA_CurrentBoostFinish",
            pipeline_override={
                "MCA_CurrentBoostFinalFlag": {"expected": str(final_boost)}
            },
        )
        ########################################
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="完成灵力点使用")


@AgentServer.custom_recognition("MCA_ActionChooseTarget")
class MCA_ActionChooseTarget(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        print("##########_##########_##########")
        
        target_order = int(json.loads(argv.custom_recognition_param)["target_order"])
        target_order_name = str(json.loads(argv.custom_recognition_param)["target_order_name"])
        if not target_order_name:
            # print(f"target_order is {target_order}")
            logger.info(f"target_order is {target_order}")
            for _ in range(2):
                if target_order == 1:
                    context.tasker.controller.post_click(229, 346)
                if target_order == 2:
                    context.tasker.controller.post_click(362, 270)
                if target_order == 3:
                    context.tasker.controller.post_click(491, 232)
                time.sleep(0.5)
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="完成切换目标")
        # print(f"target_order_name is {target_order_name}")
        logger.info(f"target_order_name is {target_order_name}")
        current_name = None
        while not current_name == target_order_name:
            if target_order == 1:
                context.tasker.controller.post_click(229, 346)
            if target_order == 2:
                context.tasker.controller.post_click(362, 270)
            if target_order == 3:
                context.tasker.controller.post_click(491, 232)
            reco_detail = context.run_task("MCA_ChooseTargetStart")
            current_name = str(reco_detail.nodes[0].recognition.all_results[0].text)
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="完成技能")


@AgentServer.custom_recognition("MCA_ActionShield")
class MCA_ActionShield(CustomRecognition):
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
        print("##########_##########_##########")
        shield_number_use = int(json.loads(argv.custom_recognition_param)["shield_number"])
        if shield_number_use <= 0:
            # print(f"use 0 bullet")
            logger.info(f"use 0 bullet")
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="不使用擦弹")
        # print(f"use {shield_number_use} bullet")
        logger.info(f"use {shield_number_use} bullet")
        reco_detail = context.run_recognition("MCA_GetShieldNumber", argv.image)
        if not reco_detail:
            shield_number = 0
        else:
            shield_number = len(reco_detail.filterd_results)
        bullet_target_number = shield_number + shield_number_use
        if bullet_target_number >= 5:
            bullet_target_number = 4

        context.run_task(
            "MCA_ShieldLine",
            pipeline_override={
                "MCA_GetShieldFinishFlag": {"index": int(bullet_target_number) - 1}
            },
        )
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="finish")


@AgentServer.custom_recognition("MCA_ActionSpellCardUse")
class MCA_ActionSpellCardUse(CustomRecognition):
    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        """
        :param context:
        :param argv:node_name
                    custom_recognition_name
                    custom_recognition_param
                    image
                    roi
        :return:
        """
        print("##########_##########_##########")
        spell_card_list = [
            {"box": [151, 423, 57, 33]},
            {"box": [330, 318, 55, 27]},
            {"box": [523, 250, 56, 26]},
            {"box": [722, 208, 56, 27]},
            {"box": [930, 185, 55, 32]},
            {"box": [326, 604, 212, 45]},
            {"box": [741, 602, 220, 49]}
        ]
        target_SpellCard = int(json.loads(argv.custom_recognition_param)["target_SpellCard"])
        roi = spell_card_list[target_SpellCard - 1]["box"]
        if target_SpellCard == 6 or target_SpellCard == 7:
            # print(f"use normal attack {target_SpellCard - 5}")
            logger.info(f"use normal attack {target_SpellCard - 5}")
            context.tasker.controller.post_click(
                int(roi[0] + roi[2] / 2), int(roi[1] + roi[3] / 2)
            ).wait()
            return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="完成平a使用")
        # print(f"use {target_SpellCard} card")
        logger.info(f"use {target_SpellCard} card")
        context.run_task("MC_OpenSpellCardList")

        context.tasker.controller.post_click(
            int(roi[0] + roi[2] / 2), int(roi[1] + roi[3] / 2)
        ).wait()
        

        # reco_detail = context.run_task("MCA_GetSpellCardLocation")
        # context.run_task(
        #     "MCA_SpellCardClickOne",
        #     pipeline_override={
        #         "MCA_SpellCardClick": {
        #             "roi": reco_detail.nodes[0].recognition.filterd_results[target_SpellCard - 1].box}
        #     },
        # )
        return CustomRecognition.AnalyzeResult(box=[0, 0, 0, 0], detail="完成符卡使用")
