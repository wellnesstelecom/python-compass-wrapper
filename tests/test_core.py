#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase
from validators import Compile, ValidationError
from compass import Compass


class TempDirEnvironmentMixin(object):

    def load_dir(self):
        import tempfile
        import os
        self.temp_dir = tempfile.mkdtemp(prefix='test_compass')
        self.sass_dir = os.path.join(self.temp_dir, 'sass')
        self.css_dir = os.path.join(self.temp_dir, 'css')
        os.mkdir(self.sass_dir)
        os.mkdir(self.css_dir)


class TestCompileValidator(TempDirEnvironmentMixin, TestCase):

    def setUp(self):
        self.load_dir()

    def test_correct_args(self):
        config = {
            'sass_dir': self.sass_dir,
            'css_dir': self.css_dir,
            'fake_arg': 'test',
            1: 2,
            3: True,
            4: False,
            'boring': True,
            'relative_assets': False,
            'images_dir': '',
        }
        validator = Compile(config)
        self.assertEquals(validator, {
            'sass_dir': self.sass_dir,
            'css_dir': self.css_dir,
            'boring': True,
            'relative_assets': False,
            'images_dir': '',
        })

    def test_incorrect_args(self):
        config = {
            'sass_dir': '/path/to/nothing/',
        }
        self.assertRaises(ValidationError, Compile, config)
        config = {
            'sass_dir': '/path/to/nothing/',
            'css_dir': self.css_dir,
        }
        self.assertRaises(ValidationError, Compile, config)


class TestCompass(TempDirEnvironmentMixin, TestCase):

    def setUp(self):
        self.load_dir()
        self.compass = Compass()

    def test_compile(self):
        config = {
            'sass_dir': self.sass_dir,
            'css_dir': self.css_dir,
            'boring': True,
            'quiet': True,
            'output_style': 'extended',
        }
        self.compass.config = config
        output = self.compass.compile()
        pass
