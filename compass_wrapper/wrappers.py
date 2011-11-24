#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
from compass_wrapper.exceptions import CompassError
import os

BINARY = 'compass'


class Wrapper(object):

    _command = [BINARY]
    _extra_args = []

    def __init__(self, parser):
        self.parser = parser

    def __call__(self):
        command = self._command + self.parser.dumps() + self.extra_args
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

    @property
    def extra_args(self):
        return self._extra_args

    @extra_args.setter
    def extra_args(self, value):
        self._extra_args.append(str(value))

class Compile(Wrapper):

    _command = [BINARY, 'compile']

    def select(self, name, in_dir=None):
        sass_dir_in_config = self.parser.validator.get('sass_dir')
        search_file = "%s.sass" % name
        assert sass_dir_in_config  # if assert, it's a bug
        for root, dirs, files in os.walk(os.path.join(
            sass_dir_in_config, in_dir or '')):
            if search_file in files:
                self.extra_args = os.path.join(root, search_file)
                return True

        raise CompassError("Can't find '%s' into '%s' (recursive)"
            % (search_file, sass_dir_in_config))
