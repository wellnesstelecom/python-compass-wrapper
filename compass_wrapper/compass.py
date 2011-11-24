#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from compass_wrapper.wrappers import Wrapper
from compass_wrapper import validators, parsers


class Compass(object):

    def __init__(self, config=None):
        if config:
            self.config = config

    @property
    def compile(self):
        parser = parsers.Compile(validators.Compile(self.config))
        return Wrapper(parser)
