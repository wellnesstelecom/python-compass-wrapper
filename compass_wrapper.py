#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
import os
from validators import Compile

BINARY = 'compass'
COMPRESSED = 'nested, expanded, compact, compressed'

class Wrapper(object):

    _command = [BINARY]

    def __init__(self, config=None):
        if config:
            self._config = config

    def config(self):
        raise NotImplementedError('It need subclass')

    def _args_parsed(self):
        options = []
        for arg, value in self.config.items():
            options.append("--%s=%s" % (
                    arg.replace('_','-').lower(),
                    value
                ))
        return options

    def __call__(self):
        command = self._command + self._args_parsed()
        try:
            output = subprocess.check_output(command)
        except Exception as e:
            output = e
        return output

class Compiler(Wrapper):

    def __init__(self, config=None):
        self._command.append('compile')
        super(Compiler, self).__init__(config)

    @property
    def config(self):
        return Compile(self._config)
