#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class Validator(dict):
    """ Abstract subclass of dict """

    def __init__(self, dict=None):
        if dict and hasattr(dict, 'items'):
            for k, v in dict.items():
                self[k] = v
        super(Validator, self).__init__(self)

    def __setitem__(self, name, value):
        if name in self._valid_args:
            super(Validator, self).__setitem__(name, value)

    def update(self, D, **kwargs):
        D = self.__class__(D)
        super(Validator, self).update(D)

class Compile(Validator):

    _valid_args = (
        'quiet', 'boring', 'sass_dir', 'css_dir', 'images_dir',
        'javascripts_dir', 'relative_assets', 'no_line_comments',
        'output_style')
