#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8134995961:AAE09kn2ajdDLjzemOuW4IYTbVIOGx_hgxk")
    API_ID = int(os.environ.get("API_ID", "20834791"))
    API_HASH = os.environ.get("API_HASH", "549eef0fbfbbf52140fa6408435d034b")
    AUTH_USERS = os.environ.get("AUTH_USERS", "6404676836")
