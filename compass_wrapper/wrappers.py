#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
from compass_wrapper.exceptions import CompassError

BINARY = 'compass'


class Wrapper(object):

    _command = [BINARY]

    def __init__(self, parser):
        self._command.append('compile')
        self.parser = parser

    def __call__(self):
        command = self._command + self.parser.dumps()
        try:
            output = subprocess.check_output(
                ' '.join(command), stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as call_error:
            raise CompassError("""'%s' fails:
                %s""" % (call_error.cmd, call_error.output))
        except OSError as os_error:
            raise CompassError("Did you install compass?: '%s' returns: %s"
                % (' '.join(command), os_error))
        return output
