#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from compass_wrapper.compass import Compass
from compass_wrapper.validators import Compile
from compass_wrapper.exceptions import ValidatorError, CompassError
from fixtures import *
from unittest import TestCase
import os

class TempDirEnvironmentMixin(object):

    def load_dir(self):
        import tempfile
        self.temp_dir = tempfile.mkdtemp(prefix='test_compass')
        self.sass_dir = os.path.join(self.temp_dir, 'sass')
        self.css_dir = os.path.join(self.temp_dir, 'css')
        os.mkdir(self.sass_dir)
        os.mkdir(self.css_dir)

    def load_sass(self, name='test', content=None):
        with open(os.path.join(self.sass_dir, "%s.sass" % name), 'w') as sass:
            sass.write(content)

    def list_sass(self):
        return filter(
            lambda x: x.endswith('sass'),
            os.listdir(self.sass_dir))

    def list_css(self):
        return filter(
            lambda x: x.endswith('css'),
            os.listdir(self.css_dir))


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
        self.assertRaises(ValidatorError, Compile, config)
        config = {
            'sass_dir': '/path/to/nothing/',
            'css_dir': self.css_dir,
        }
        self.assertRaises(ValidatorError, Compile, config)


class TestCompass(TempDirEnvironmentMixin, TestCase):

    def setUp(self):
        self.load_dir()
        self.load_sass(name='test1', content=SASS1)
        self.compass = Compass()

    def test_compile(self):
        config = {
            'sass_dir': self.sass_dir,
            'css_dir': self.css_dir,
            'boring': True,
            'quiet': True,
            'output_style': 'compressed',
        }
        self.compass.config = config
        output = self.compass.compile()
        self.assertEquals(self.list_css(), ['test1.css'])
        with open(os.path.join(self.css_dir, 'test1.css')) as css:
            self.assertEquals(css.read(), "body{color:red}body a{color:blue}\n")

        self.load_sass(name='test2', content=SASS2)
        self.assertRaises(CompassError, self.compass.compile)
