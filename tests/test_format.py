import sys
import os
import platform
import pdb
import unittest
from unittest.mock import MagicMock

import sublime
import sublime_plugin

from . import sbot_common as sc
from SbotFormat import sbot_format
from SbotHighlight import sbot_highlight
from Notr import notr, table


# TODO1 relocate to other packages.


# Experiments with testing py code in general and ST plugins specifically.

# print(f'Running {__file__} with python {platform.python_version()} on {platform.platform()}')


# Exclude unittests from production builds
# ->
# # git
# .github/ export-ignore
# .git export-ignore
# .gitignore export-ignore
# .gitattributes export-ignore
# # development utilities
# /dev/ export-ignore
# .travis.yml export-ignore
# tox.ini export-ignore
# # unittests
# tests/ export-ignore
# # example files
# /example-*.json export-ignore

# Add root unittesting.json:
# {
#     "tests_dir": "package_control/tests",
#     "pattern": "test*.py",
#     "verbosity": 1
# }



#-----------------------------------------------------------------------------------
class TestFormat(unittest.TestCase):

    def setUp(self):
        mock_settings = {
            "tab_size": 4,
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

    def tearDown(self):
        pass

    def test_format_json(self):
        v = sublime.View(601)

        with open(r'SbotDev\test_files\messy.json', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatJsonCommand(v)
            res = cmd._do_one(s)
            self.assertEqual(res[:50], '{\n    "MarkPitch": {\n        "Original": 0,\n      ')

            # Make it a bad file.
            s = s.replace('\"Original\"', '')
            res = cmd._do_one(s)
            self.assertEqual(res[:50], "Json Error: Expecting property name enclosed in do")

    def test_format_xml(self):
        v = sublime.View(602)

        with open(r'SbotDev\test_files\messy.xml', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatXmlCommand(v)
            res = cmd._do_one(s, '    ')

            if 'Error:' in res:
                self.fail(res)
            else:
                self.assertEqual(res[100:150], 'nType="Anti-IgG (PEG)" TestSpec="08 ABSCR4 IgG" Du')

            # Make it a bad file.
            s = s.replace('ColumnType=', '')
            res = cmd._do_one(s, '    ')
            self.assertEqual(res, "Error: not well-formed (invalid token): line 6, column 4")
