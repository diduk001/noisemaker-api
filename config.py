import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b50f19617f114c3fb0db6ae3a8937332'
