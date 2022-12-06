# -*- coding:utf-8 -*-
import logging
import logging.config
import os
import sys
from collections import namedtuple

DEBUG = False
log_level = logging.DEBUG if DEBUG else logging.INFO
RootPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
InfoLogPath = os.path.join(RootPath, "./logs/info.log")
WarningLogPath = os.path.join(RootPath, "./logs/warn.log")
ErrorLogPath = os.path.join(RootPath, "./logs/error.log")

log_config_dict = {
    "version": 1,
    'disable_existing_loggers': True,

    'loggers': {
        'log.info': {
            'handlers': ['console'] if DEBUG else ['info', 'console'],
            'level': log_level,
            'propagate': False,  # 是否传递给父记录器
        },
        'log.warning': {
            'handlers': ['console'] if DEBUG else ['warning', 'console'],
            'level': logging.WARNING,
            'propagate': False,  # 是否传递给父记录器
        },
        'log.error': {
            'handlers': ['console'] if DEBUG else ['error', 'console'],
            'level': logging.ERROR,
            'propagate': False,  # 是否传递给父记录器
        },
        'tornado.access': {
            'handlers': ['console'],
            'level': logging.INFO,
            'propagate': False,  # 是否传递给父记录器
        },
    },

    'handlers': {
        # 输出到控制台
        'console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout
        },
        # 输出到文件
        'info': {
            'level': log_level,
            'class': 'logging.handlers.TimedRotatingFileHandler',   # todo 更换一个handle 确保多进程不丢日志
            'formatter': 'standard',
            'filename': InfoLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8'
        },
        'warning': {
            'level': logging.WARNING,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': WarningLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8',
        },
        'error': {
            'level': logging.ERROR,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': ErrorLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8',
        },
    },
    'filters': {},
    'formatters': {
        # 标准输出格式
        'standard': {
            # 'format': '[%(asctime)s] - %(levelname)s %(module)s:%(funcName)s(%(lineno)d) - %(message)s'
            'format': '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        }
    }
}

logging.config.dictConfig(log_config_dict)

info = logging.getLogger("log.info")
warning = logging.getLogger("log.warning")
error = logging.getLogger("log.error")

log_ = namedtuple('log', ["info", "warning", "error"])
log = log_(info=info.info, warning=warning.warning, error=error.error)
