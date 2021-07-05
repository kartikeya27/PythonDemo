import configparser
import string
import random


def getConfig():
    config = configparser.ConfigParser()
    config.read('utilities/properties.ini')
    return config
