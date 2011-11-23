#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from wrappers import Wrapper
import validators
import parsers


class Compass(object):

    def __init__(self, config=None):
        if config:
            self.config = config

    @property
    def compile(self):
        parser = parsers.Compile(validators.Compile(self.config))
        return Wrapper(parser)
