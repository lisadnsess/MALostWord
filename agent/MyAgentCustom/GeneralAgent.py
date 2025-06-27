# -*- coding: utf-8 -*-
import os
import sys


def run_task_param(new_ctx, action_name, param_name=None, param_data=None):
    # print(param_data)
    # print(type(param_data))
    if not param_name and not param_data:
        new_ctx.run_task(action_name)

    if type(param_data) is dict:
        new_ctx.run_task(
            action_name,
            pipeline_override=
            {action_name: {"custom_recognition_param": param_data}}
        )
    else:
        new_ctx.run_task(
            action_name,
            pipeline_override=
            {action_name: {"custom_recognition_param": {param_name: param_data}}}
        )
    pass


class SuppressOutput:
    """上下文管理器：临时屏蔽所有 print 输出"""

    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self.original_stdout
