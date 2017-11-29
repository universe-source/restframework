"""
小功能, 帮助函数
"""
import os
import binascii


def gen_fake_email():
    name = binascii.hexlify(os.urandom(7)).decode()
    return '{}@fake.xinshu.me'.format(name)


def gen_fake_phone():
    name = binascii.hexlify(os.urandom(7)).decode()
    return '{}@'.format(name)


def gen_fake_username():
    return binascii.hexlify(os.urandom(5)).decode()


def is_fake_email(email):
    return email.endswith('@fake.xinshu.me')


def is_fake_phone(phone):
    return phone.endswith('@')
