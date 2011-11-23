#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase
from validators import Compile
from compass_wrapper import Compiler

class TestCompileValidator(TestCase):

    def setUp(self):
        self.compile_args = Compile()

    def test_add_correct_args(self):
        self.compile_args.update({
            'sass_dir': '',
            'css_dir': '',
            'output_style': '',
        })
        self.assertEquals(len(self.compile_args), 3)
        self.compile_args['quiet'] = True
        self.assertEquals(len(self.compile_args), 4)

    def test_add_incorrect_args(self):
        self.compile_args.update({
            'fake_arg': 1,
            2: 2,
            'boring': True,
            'sass_dir': 'some_path',
        })
        self.assertEquals(len(self.compile_args), 2)

class TestCompiler(TestCase):

    def setUp(self):
        compile_args = {
            'boring': True,
            'relative_assets': True
        }
        self.compiler = Compiler(compile_args)

    def test_compiler_init(self):
        self.assertIsInstance(self.compiler.config, Compile)
        self.assertEquals(self.compiler._args_parsed(), [
            '--boring=True', '--relative-assets=True'])

    def test_call(self):
        output = self.compiler()
        self.assertTrue(output.returncode, 1)
