# -*- coding: utf-8 -*-
import sys
from .test_DM import DMA_Print, DMA_Logger, DMA_GetDate, DMA_DailyMaterialAll
from .test_UF import UF_Logger, UF_Count, UF_CountClean, UF_RecognitionCustom, UF_ChangePipeline, UF_RunPipeline
from .test_AUF import UF_ActionLogger, UF_ActionRunPipeline
from .test_MC import MCA_ActionOneScreen, MCA_ActionSkillOpen, MCA_ActionChangeCharacter, MCA_ActionBoost, \
    MCA_ActionChooseTarget, MCA_ActionShield, MCA_ActionSpellCardUse
from .test_EF import EFA_ActionAll
from .test_SR import SRA_ActionSpiritRevival

from .test_AMC import MCA_LoadFightStrategy, MCA_UseSkill, MCA_Round, MCA_UseBoost
from .test_RMC import MCR_UseShield

# 显式列出需要处理的函数
FUNCTIONS_RECOGNITION = [
    # 来自 test_DM 的函数
    DMA_Print,
    DMA_Logger,
    DMA_GetDate,
    DMA_DailyMaterialAll,
    # 来自 test_UF 的函数
    UF_Logger,
    UF_Count,
    UF_CountClean,
    UF_RecognitionCustom,
    UF_ChangePipeline,
    UF_RunPipeline,

    # 来自 test_EF 的函数
    EFA_ActionAll,

    # 来自 test_SR 的函数
    SRA_ActionSpiritRevival,

    # 来自 test_MC 的函数
    MCA_ActionOneScreen,
    MCA_ActionSkillOpen,
    MCA_ActionChangeCharacter,
    MCA_ActionBoost,
    MCA_ActionChooseTarget,
    MCA_ActionShield,
    MCA_ActionSpellCardUse,

    # 来自 test_RMC 的函数
    MCR_UseShield,

]

FUNCTIONS_ACTION = [
    # 来自 test_AUF 的函数
    UF_ActionLogger,
    UF_ActionRunPipeline,

    # 来自 test_AMC 的函数
    MCA_LoadFightStrategy,
    MCA_Round,
    MCA_UseSkill,
    MCA_UseBoost,
]

flag = getattr(sys.modules["__main__"], "Agent_FLAG", True)
if flag:
    from maa.agent.agent_server import AgentServer

    for func in FUNCTIONS_RECOGNITION:
        decorated_func = AgentServer.custom_recognition(func.__name__)(func)
        globals()[func.__name__] = decorated_func

    for func in FUNCTIONS_ACTION:
        decorated_func = AgentServer.custom_action(func.__name__)(func)
        globals()[func.__name__] = decorated_func
    __all__ = [func.__name__ for func in FUNCTIONS_RECOGNITION]  # 添加实例到导出列表
else:
    from maa.resource import Resource

    resource = Resource()
    for func in FUNCTIONS_RECOGNITION:
        decorated_func = resource.custom_recognition(func.__name__)(func)
        globals()[func.__name__] = decorated_func

    for func in FUNCTIONS_ACTION:
        decorated_func = resource.custom_action(func.__name__)(func)
        globals()[func.__name__] = decorated_func
    __all__ = [func.__name__ for func in FUNCTIONS_RECOGNITION] + ["resource"]  # 添加实例到导出列表
# 定义导出列表：包含所有函数和recognition_handler实例
