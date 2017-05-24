#!/usr/bin/env python
# -*- coding=utf-8 -*-

from os import access, path, R_OK
import os
import logging
from logging.config import fileConfig


log_config_path =  os.path.join(os.path.dirname(os.getcwd()), 'config', 'logging.conf')
if path.exists(log_config_path) and path.isfile(log_config_path) and access(log_config_path, R_OK):
    logging.config.fileConfig(log_config_path)

log_config_path =  os.path.join('/etc/tumbler/logging.conf')
if path.exists(log_config_path) and path.isfile(log_config_path) and access(log_config_path, R_OK):
    logging.config.fileConfig(log_config_path)

logger = logging.getLogger('simple')
