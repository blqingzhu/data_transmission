#! /usr/bin/env python
# -*- coding: UTF-8 -*-


"""
只是需要测试报告组件，不需要utx的其他扩展功能
"""
import os

from utx import *

if __name__ == '__main__':
    utx.stop_patch()
    case_path = os.path.basename(os.getcwd())
    title="测试"
    runner = TestRunner("title",case_path)
    except_fileList=[]
    runner.run_test(except_fileList)
