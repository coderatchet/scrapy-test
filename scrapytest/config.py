# -*- coding: utf-8 -*-
"""
    config.py

    loads the configuratio based off environment settings and saves it in a variable named ``config``

    exits program if configuration load failed.

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

import json
import os

import logging

from scrapytest.utils import merge_dict

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
config_file_path = os.path.join(root_dir, 'config.json')

# load the default configuration
try:
    with open(config_file_path) as file:
        default_config_data = file.read()
        config = json.loads(default_config_data)

        # load the custom environment configuration over the original
        env = os.getenv('ENV', None)
        env_config_file = os.path.join(root_dir, 'config.' + str(env) + '.json')
        if env and os.path.exists(env_config_file):
            with open(env_config_file) as env_file:
                env_config_data = env_file.read()
                env_config = json.loads(env_config_data)
                config = merge_dict(env_config, config)
except Exception as e:
    logging.log(logging.CRITICAL, "could not load configuration!!!\n{}".format(e))
    exit(1)
