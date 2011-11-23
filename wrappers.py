#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess

BINARY = 'compass'

class Wrapper(object):

    _command = [BINARY]

    def __init__(self, parser):
        self._command.append('compile')
        self.parser = parser

    def __call__(self):
        command = self._command + self.parser.dumps()
        print ' '.join(command)
        try:
            output = subprocess.check_output(command)
        except Exception as e:
            output = e
        return output
