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

    def tearDown(self):
        from shutil import rmtree
        rmtree(self.temp_dir)


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
        config = {
            'sass_dir': self.sass_dir,
            'css_dir': self.css_dir,
            'output_style': 'fake',
        }
        self.assertRaises(ValidatorError, Compile, config)


class TestCompass(TempDirEnvironmentMixin, TestCase):

    def setUp(self):
        self.load_dir()
        self.load_sass(name='test1', content=SASS1)
        self.compass = Compass({
            'sass_dir': self.sass_dir,
            'css_dir': self.css_dir,
            'boring': True,
            'quiet': True,
            'output_style': 'compressed',
        })

    def test_compile(self):
        output = self.compass.compile()
        self.assertEquals(self.list_css(), ['test1.css'])
        with open(os.path.join(self.css_dir, 'test1.css')) as css:
            self.assertEquals(css.read(), "body{color:red}body a{color:blue}\n")

        self.load_sass(name='test2', content=SASS2)
        self.assertRaises(CompassError, self.compass.compile)

    def test_compile_file(self):
        self.load_sass(name='test2', content=SASS3)
        self.compass.compile_file('test2.sass')
        self.assertEquals(self.list_css(), ['test2.css'])
        self.assertRaises(CompassError, self.compass.compile_file, 'fake')

    def test_compile_file_with_deep(self):
        os.mkdir(os.path.join(self.sass_dir, 'dir1'))
        os.mkdir(os.path.join(self.sass_dir, 'dir1', 'dir2'))
        into_dir = os.path.join('dir1', 'dir2', 'deep')
        self.load_sass(name=into_dir, content=SASS1)
        self.compass.compile_file('deep.sass')
        self.assertEquals(os.listdir(
            os.path.join(self.css_dir, 'dir1/dir2')), ['deep.css'])

    def test_compile_file_with_two_equals(self):
        """
        /sass_dir/dir/into1/deep.sass
        /sass_dir/dir/into2/deep.sass
        """
        parent_dir = os.path.join(self.sass_dir, 'dir')
        os.mkdir(parent_dir)
        os.mkdir(os.path.join(parent_dir, 'into1'))
        os.mkdir(os.path.join(parent_dir, 'into2'))
        self.load_sass(
            name=os.path.join('dir', 'into1', 'deep'), content=SASS1)
        self.load_sass(
            name=os.path.join('dir', 'into2', 'deep'), content=SASS1)
        self.compass.compile_file('dir/into1/deep.sass')
        self.assertEquals(os.listdir(
            os.path.join(self.css_dir, 'dir/into1')), ['deep.css'])
        self.assertEquals(os.listdir(
            os.path.join(self.css_dir, 'dir')), ['into1'])
