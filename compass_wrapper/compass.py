#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from compass_wrapper.wrappers import Compile
from compass_wrapper.exceptions import CompassError
from compass_wrapper import validators, parsers


class Compass(object):

    def __init__(self, config=None):
        self.config = config or {}

    def _get_compile_wrapper(self):
        parser = parsers.Compile(validators.Compile(self.config))
        return Compile(parser)

    @property
    def compile(self):
        return self._get_compile_wrapper()

    def compile_file(self, name_file):
        compiler = self._get_compile_wrapper()
        compiler.select(name_file)
        compiler()
