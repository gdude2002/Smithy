# coding=utf-8
from yaml import safe_load

__author__ = "Gareth Coles"

config = safe_load(open("config.yml"))

TOKEN = config["token"]
DATABASE = config["db"]
