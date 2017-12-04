# coding:utf8
"""
    关于错误码返回,要么都是用 HTTP 错误码, 要么全部返回200, 然后使用自定义错误码,
    避免混乱和模糊不清.
"""

from .auth import *
from .user import *
from .mail import *
from .ticket import *


messages = {}
for name in dir():
    if name.startswith('CODE_') and not name.endswith('_MSG'):
        messages[globals()[name]] = globals()[name + '_MSG']
