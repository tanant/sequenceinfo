import unittest
import inspect
import re

from sequenceinfo.splitter import Splitter
import sequenceinfo.pattern_library as pattern_library

# hmm.. what happens if a user puts in a pattern that splits the digit section
# with some non digits in it? Could happen. What's the result of this? can we
# even manage it? That might be making the splitter too smart.
#
# Perhaps the sequencer mux will support this instead
#

# force set: set(rec.groupindex.keys()) to


"""
in long form, the splitter is a class, that can has the following interface
.patterns : returns a list of RE compiled objects that are used to split strings)
.add_pattern(pattern_string, at_head = True) : convenience function that takes a re-compileable string
                                  to add to the pattern match list.
.split(string) :  function to split the given string along the patterns, returning a head/pad/tail tuple

this module can be initialised with no parameters, or an optional list of RE split strings that are
defined in the class
"""

STRING_NOTYETIMPLEMENTED = "not yet implemented"


class TestInterface(unittest.TestCase):
    """
    package of tests to ensure presence and method signatures.
    """
    PATTERN_simple = r'(?P<head>potato\.)(?P<digits>[0-9]+)(?P<tail>\.chips)'
    PATTERN_extra_groups = r'(?P<head>potato\.)(?P<digits>[0-9]+)(?P<tail>\.chips)(?P<foo>.exr)'
    PATTERN_missing_groups = r'potato\.[0-9]+\.chips'
    PATTERN_non_digit_filled_digit_match = r'(?P<head>potato\.)(?P<digits>junk[0-9]+)(?P<tail>\.chips)'

    def setUp(self):
        self.splitter = Splitter()

    def test_can_return_patterns(self):
        # implementation detail?
        # assumes that we use compiled RE objects as our patterns...
        self.assertTrue(hasattr(self.splitter, "patterns"),
                        "cannot find 'patterns' attribute")

        # I feel like i should be testing for presence of the .match() method,
        # rather than if it's a compiled re?
        self.assertTrue(all([isinstance(x, type(re.compile(''))) for x in self.splitter.patterns]),
                        "patterns returned are not of a valid type")

    def test_add_pattern_signature(self):
        self.assertEquals(inspect.getargspec(self.splitter.add_pattern).args, ["self", "pattern_string", "at_head"],
                          "function signature wrong")

        self.assertEquals(
            inspect.getargspec(self.splitter.add_pattern).defaults, (True,),
                               "function signature defaults wrong")

    def test_default_patterns_exist(self):
        self.assertTrue(len(self.splitter.patterns) > 0,
                        "no default patterns")

    def test_has_split_function(self):
        self.assertTrue(hasattr(self.splitter, "split_string"))

    def test_can_add_pattern(self):
        self.assertTrue(hasattr(self.splitter, "add_pattern"),
                        "cannot find 'patterns' attribute")

        self.assertTrue(self.splitter.add_pattern(self.PATTERN_simple),
                        "can't add in good form pattern")

        # nothing wrong with double adding pattern, aside from storage/speed penalty
        # self.assertTrue(self.splitter.add_patternself.PATTERN_simple),
        #                "can't add in good form pattern")

        with self.assertRaises(ValueError):
            self.splitter.add_pattern(self.PATTERN_extra_groups)

        with self.assertRaises(ValueError):
            self.splitter.add_pattern(self.PATTERN_missing_groups)

        # I don't know if we can test this to be honest, caveat emptor for this
        # particular case
        #with self.assertRaises(ValueError):
        #    self.splitter.add_pattern(self.PATTERN_non_digit_filled_digit_match)


class TestPatternMatches(unittest.TestCase):
    """
    These tests assume that the interface is good, so they specifically hammer
    the pattern engine to make sure that the input/output pairings are good.

    I expect this module to expand to cover a LOT of input ramming
    """
    simple_digit_test_data = [ ("file.123123.exr", ("file.", "123123", ".exr")),
                               ("fool.123.file.123123.exr", ("fool.123.file.", "123123", ".exr")),
                               ("file.012.exr", ("file.", "012", ".exr")),
                              ]
    dcf_test_data = [("IMG_1234.foo", ("IMG_", "1234", ".foo")),
                     ("DCIM1234.foo", ("DCIM", "1234", ".foo")),
                     ("DSC01234.foo", ("DSC0", "1234", ".foo")),
                     ("_DSC01234.foo", ("_DSC0", "1234", ".foo")),
                       ]
    def setUp(self):
        self.splitter = Splitter()
        self.splitter.patterns = []

    def test_simple_digit_split(self):

        test_tuples = self.simple_digit_test_data
        bad_test_tuples = self.dcf_test_data
        self.splitter.add_pattern(pattern_library.digits_with_optional_dots)

        for index, tuple in enumerate(test_tuples):
            self.assertEqual(self.splitter.split_string(tuple[0]), tuple[1],
                            "did not split input {x} successfully (expected: {expect}, got: {res})".format(x=index, expect=tuple[1], res=self.splitter.split_string(tuple[0])))

        for index, tuple in enumerate(bad_test_tuples):
            self.assertEqual(self.splitter.split_string(tuple[0]), (tuple[0], None, None),
                            "did not split input {x} successfully (expected: {expect}, got: {res})".format(x=index, expect=tuple[1], res=self.splitter.split_string(tuple[0])))


    def test_dcf_format_digital_stills(self):
        test_tuples = self.dcf_test_data
        self.splitter.add_pattern(pattern_library.dcf_format_digital_stills)

        for index, tuple in enumerate(test_tuples):
            self.assertEqual(self.splitter.split_string(tuple[0]), tuple[1],
                             "did not split input {x} successfully (expected: {expect}, got: {res})".format(
                                 x=index, expect=tuple[1],
                                 res=self.splitter.split_string(tuple[0])))


# TODO: make sure pattern match precedence works
# TODO: better way to remove patterns? (or just force manip of the list)