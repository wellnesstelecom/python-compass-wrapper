#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class Parser(object):

    def __init__(self, validator):
        self.validator = validator or []

    def dumps(self):
        result = []
        for arg, value in self.validator.items():
            if not value: continue
            result.append("--%s %s" % (
                arg.replace('_','-'),
                '' if isinstance(value, bool) else str(value)))
        return map(lambda x: x.strip(), result)

class Compile(Parser):
    pass
