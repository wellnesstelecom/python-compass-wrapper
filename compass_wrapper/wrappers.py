#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from compass_wrapper.exceptions import CompassError
import os
import oversubprocess

BINARY = 'compass'


class Wrapper(object):

    _command = [BINARY]

    def __init__(self, parser):
        self.parser = parser
        self._extra_args = []

    def __call__(self):
        command = self._command + self.parser.dumps() + self.extra_args
        try:
            output = oversubprocess.check_output(' '.join(command), shell=True)
        except oversubprocess.CalledProcessError as call_error:
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

    def _parse_file(self, name):
        """ Return in_dir, search file """
        if '/' in name:
            bits = name.split('/')
            return (os.path.join(*bits[0:-1]), bits[-1])
        else:
            return None, name

    def select(self, name):
        # TODO: Do I must forget recursive search? What if there are two files with equals name?
        sass_dir_in_config = self.parser.validator.get('sass_dir')
        assert sass_dir_in_config  # if assert, it's a bug
        in_dir, search_file = self._parse_file(name)
        for root, dirs, files in os.walk(os.path.join(
            sass_dir_in_config, in_dir or '')):
            if search_file in files:
                self.extra_args = os.path.join(root, search_file)
                return True

        raise CompassError("Can't find '%s' into '%s' (recursive)"
            % (search_file, sass_dir_in_config))
