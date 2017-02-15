# -*- coding: utf-8 -*-
"""
    config.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

import json
import os

config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'config.json')
default_config_data = open(config_file_path).read()
config = json.loads(default_config_data)
