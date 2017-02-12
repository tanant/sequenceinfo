"""
This is a container for the two (three?) major building blocks. It can be later
broken out into a proper module if desired, but for now, simplicity wins
"""

import logging
logger = logging.getLogger(__name__)

import inspect
import re
import pattern_library

# TODO: splitter should have it's own sane library of patterns.
#       custom patterns are LOW GUARANTEE objects, as in, they may end up giving
#       you non-safe matches

# patterns must take the form of RE compiled strings that have three groups


class Splitter(object):
    def __init__(self):
        self.patterns = []
        self.add_pattern(pattern_library.digits_with_optional_dots)

    def add_pattern(self, pattern_string, at_head=True):
        compiled_pattern = re.compile(pattern_string)
        if set(compiled_pattern.groupindex.keys()) == set(['digits', 'head', 'tail']):
            pass
        else:
            raise ValueError("Supplied pattern does not conform, it must only have three named groups: 'digits', 'head', 'tail' ")

        if at_head:
            self.patterns.insert(0, compiled_pattern)
        else:
            self.patterns.append(compiled_pattern)
        return compiled_pattern

    def split_string(self, string_to_split):
        match = None
        for pattern in self.patterns:
            match = pattern.match(string_to_split)
            if match:
                break
        if match is None:
            return (string_to_split,None,None)
        else:
            return (match.group('head'), match.group('digits'), match.group('tail'))