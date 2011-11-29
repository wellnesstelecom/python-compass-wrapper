#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from compass_wrapper.exceptions import ValidatorError
from os import path
import inspect


class Validator(dict):
    """ Abstract subclass of dict """

    def __init__(self, dict=None):
        if dict and hasattr(dict, 'items'):
            for k, v in dict.items():
                self[k] = v
        super(Validator, self).__init__(self)
        self.post_hook()

    def __setitem__(self, name, value):
        if name in self._valid_args:
            super(Validator, self).__setitem__(name, value)

    def update(self, D, **kwargs):
        D = self.__class__(D)
        super(Validator, self).update(D)

    def post_hook(self):
        def is_validate_method(member):
            member_name, callback = member
            return (member_name.startswith('validate_')
                    and inspect.ismethod(callback))
        for k, validator in filter(is_validate_method,
                                   inspect.getmembers(self)):
            validator()


class Compile(Validator):

    _valid_args = (
        'quiet', 'boring', 'sass_dir', 'css_dir', 'images_dir',
        'javascripts_dir', 'relative_assets', 'no_line_comments',
        'output_style')

    def validate_sass_dir(self):
        sass_dir = self.get('sass_dir')
        if not sass_dir:
            raise ValidatorError("sass_dir argument doesn't exists")
        if not path.exists(sass_dir):
            raise ValidatorError(
                "sass_dir: %s path doesn't exists" % sass_dir)
        if not path.isdir(sass_dir):
            raise ValidatorError(
                "sass_dir: %s path isn't a directory" % sass_dir)

    def validate_css_dir(self):
        css_dir = self.get('css_dir')
        if not css_dir:
            raise ValidatorError("css_dir argument doesn't exists")
        if not path.exists(css_dir):
            raise ValidatorError("css_dir: %s path doesn't exists" % css_dir)
        if not path.isdir(css_dir):
            raise ValidatorError(
                "css_dir: %s path isn't a directory" % css_dir)

    def validate_output_style(self):
        output_style = self.get('output_style')
        output_valid = ('nested', 'expanded', 'compact', 'compressed')
        if output_style and output_style not in output_valid:
            raise ValidatorError(
                "output_style: %s invalid. Only accept %s" % (
                    output_style, output_valid))
